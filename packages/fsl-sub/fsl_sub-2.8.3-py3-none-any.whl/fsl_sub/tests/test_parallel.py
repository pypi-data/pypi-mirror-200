#!/usr/bin/python
import copy
import os
import os.path
import unittest
import fsl_sub.parallel
from ruamel.yaml import YAML
from tempfile import TemporaryDirectory
from unittest.mock import patch
from fsl_sub.exceptions import ArgumentError


YCONF = '''
method: shell
thread_control:
  - OMP_THREADS
  - MKL_NUM_THREADS
method_opts:
  shell:
    queues: False
    mail_support: False
    has_parallel_envs: False
    map_ram: False
    job_priorities: False
    array_holds: False
    architecture: False
    job_resources: False
    script_conf: False
    projects: False
    run_parallel: True
    parallel_disable_matches:
      - '*_gpu'
    log_to_file: True
  sge:
    queues: True
    large_job_split_pe: shmem
    has_parallel_envs: True
queues:
  short.q:
    time: 1440
    max_size: 160
    slot_size: 4
    max_slots: 16
    map_ram: true
    parallel_envs:
      - shmem
    priority: 3
    group: 1
    default: true
  long.q:
    time: 10080
    max_size: 160
    slot_size: 4
    max_slots: 16
    map_ram: true
    parallel_envs:
      - shmem
    priority: 3
    group: 2
'''
CONF = YAML(typ='safe').load(YCONF)


class TestParallelEnvs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = CONF

    def test_has_parallel_envs(self):
        config = copy.deepcopy(self.config)
        config['method_opts']['shell']['queues'] = True
        config['method_opts']['shell']['has_parallel_envs'] = True
        with self.subTest("True in config"):
            self.assertTrue(
                fsl_sub.parallel.has_parallel_envs(config=config)
            )
        with self.subTest("False in config"):
            config = copy.deepcopy(self.config)
            config['method_opts']['shell']['queues'] = True
            config['method_opts']['shell']['has_parallel_envs'] = False
            self.assertFalse(
                fsl_sub.parallel.has_parallel_envs(config=config)
            )
        with self.subTest("Missing in config - no queues"):
            config = copy.deepcopy(self.config)
            config['method_opts']['shell']['queues'] = False
            del(config['method_opts']['shell']['has_parallel_envs'])
            self.assertFalse(
                fsl_sub.parallel.has_parallel_envs(config=config)
            )
        with self.subTest("Missing in config but queue defs have parallel envs defined"):
            config = copy.deepcopy(self.config)
            config['method_opts']['shell']['queues'] = True
            del(config['method_opts']['shell']['has_parallel_envs'])
            for q, qd in config['queues'].items():
                del(config['queues'][q]['parallel_envs'])
            self.assertFalse(
                fsl_sub.parallel.has_parallel_envs(config=config)
            )

    @patch('fsl_sub_plugin_shell._to_file', return_value=True)
    def test_parallel_submit(self, *args):
        with TemporaryDirectory() as tempdir:
            # make a file with commands to run
            # parallel submit this
            # check .o and .e files
            pfile_name = "pjobs"
            cfile = os.path.join(tempdir, pfile_name)
            outputs = ['a', 'b', 'c']
            with open(cfile, 'w') as cf:
                for a in outputs:
                    cf.write("echo " + a + '\n')
            os.chdir(tempdir)
            jid = str(fsl_sub.submit(
                cfile,
                name=None,
                array_task=True))
            with self.subTest("Check output files"):
                for st in range(len(outputs)):
                    stask_id = str(st + 1)
                    of = ".".join((pfile_name, 'o' + jid, stask_id))
                    ef = ".".join((pfile_name, 'e' + jid, stask_id))
                    self.assertEqual(
                        os.path.getsize(
                            os.path.join(tempdir, ef)
                        ),
                        0
                    )
                    self.assertNotEqual(
                        os.path.getsize(
                            os.path.join(tempdir, of)
                        ),
                        0
                    )
            with self.subTest("Check .o content"):
                for st in range(len(outputs)):
                    stask_id = str(st + 1)
                    of = ".".join((pfile_name, 'o' + jid, stask_id))
                    ef = ".".join((pfile_name, 'e' + jid, stask_id))
                    with open(os.path.join(tempdir, of), 'r') as ofile:
                        output = ofile.readline()
                    self.assertEqual(output, outputs[st] + '\n')

    def test_parallel_envs(self):
        with self.subTest('Test 1'):
            self.assertListEqual(
                fsl_sub.parallel.parallel_envs(self.config['queues']),
                ['shmem', ]
            )
        with self.subTest('Test 2'):
            self.config['queues']['long.q']['parallel_envs'] = ['make', ]
            self.assertCountEqual(
                fsl_sub.parallel.parallel_envs(self.config['queues']),
                ['shmem', 'make', ]
            )
        with self.subTest('Test 3'):
            self.config['queues']['long.q']['parallel_envs'] = [
                'make', 'shmem', ]
            self.assertCountEqual(
                fsl_sub.parallel.parallel_envs(self.config['queues']),
                ['shmem', 'make', ]
            )
        with self.subTest('No parallel envs in queues'):
            test_d = copy.deepcopy(self.config)
            del test_d['queues']['long.q']['parallel_envs']
            del test_d['queues']['short.q']['parallel_envs']

            self.assertIsNone(
                fsl_sub.parallel.parallel_envs(test_d['queues'])
            )

    @patch('fsl_sub.parallel.parallel_envs')
    @patch('fsl_sub.parallel.has_parallel_envs')
    def test_process_pe_def(self, mock_hpes, mock_parallel_envs):
        mock_hpes.return_value = True
        mock_parallel_envs.return_value = ['openmp', ]
        queues = self.config['queues']
        with self.subTest('Success'):
            self.assertTupleEqual(
                ('openmp', 2, ),
                fsl_sub.parallel.process_pe_def(
                    'openmp,2',
                    queues
                )
            )
        with self.subTest('Bad input'):
            self.assertRaises(
                ArgumentError,
                fsl_sub.parallel.process_pe_def,
                'openmp.2',
                queues
            )
        with self.subTest("No PE"):
            self.assertRaises(
                ArgumentError,
                fsl_sub.parallel.process_pe_def,
                'mpi,2',
                queues
            )
        with self.subTest("No PE"):
            self.assertRaises(
                ArgumentError,
                fsl_sub.parallel.process_pe_def,
                'mpi,A',
                queues
            )
        with self.subTest("No PE"):
            self.assertRaises(
                ArgumentError,
                fsl_sub.parallel.process_pe_def,
                'mpi,2.2',
                queues
            )
        mock_hpes.return_value = False
        mock_parallel_envs.return_value = None
        with self.subTest("No PE supported, random name"):
            self.assertTupleEqual(
                (None, 2, ),
                fsl_sub.parallel.process_pe_def(
                    'nothing,2',
                    queues
                )
            )
        with self.subTest("No PE supported - blank name"):
            self.assertTupleEqual(
                (None, 2, ),
                fsl_sub.parallel.process_pe_def(
                    ',2',
                    queues
                )
            )
        with self.subTest("No PE supported - no name"):
            self.assertTupleEqual(
                (None, 2, ),
                fsl_sub.parallel.process_pe_def(
                    '2',
                    queues
                )
            )


if __name__ == '__main__':
    unittest.main()
