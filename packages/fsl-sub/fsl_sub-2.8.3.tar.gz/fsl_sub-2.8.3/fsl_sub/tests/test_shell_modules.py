#!/usr/bin/env python
import os
import unittest
import fsl_sub.shell_modules
import shutil
import subprocess
import tempfile
from unittest.mock import patch


LMOD = False
CMOD = False
if 'LMOD_CMD' in os.environ:
    LMOD = True
if shutil.which('modulecmd'):
    CMOD = True


class TestLmodSupport(unittest.TestCase):
    def setUp(self):
        os.chdir('/tmp')

    def testLmodFinder(self):
        # Look for Lmod binary
        if 'LMOD_CMD' in os.environ:
            # Test natively...
            lmod = os.environ['LMOD_CMD']
            self.assertEqual(
                fsl_sub.shell_modules.find_module_cmd(),
                lmod
            )
        else:
            with patch.dict('fsl_sub.shell_modules.os.environ', {'LMOD_CMD': '/usr/bin/lmod'}):
                self.assertEqual(
                    fsl_sub.shell_modules.find_module_cmd(),
                    '/usr/bin/lmod'
                )

    @unittest.skipUnless(LMOD, "Lmod not installed")
    def testLmodGetModules(self):
        with tempfile.TemporaryDirectory() as tempdir:
            os.mkdir(os.path.join(tempdir, 'amodule'))
            with open(os.path.join(tempdir, 'amodule', '1.0'), 'w') as amod_f:
                amod_f.write('''#%Module


proc ModulesHelp { } {
puts stderr "Defines the binary paths."
puts stderr ""
}

conflict amodule
setenv AVAR myvalue
prepend-path PATH /opt/software/A
''')
            with patch.dict(
                    'fsl_sub.shell_modules.os.environ',
                    {'MODULEPATH': tempdir, }):
                self.assertEqual(
                    fsl_sub.shell_modules.get_modules('amodule'),
                    ['1.0']
                )
            with self.subTest("Multiple versions"):
                os.mkdir(os.path.join(tempdir, 'bmodule'))
                with open(os.path.join(tempdir, 'bmodule', '1.0'), 'w') as bmod_f:
                    bmod_f.write('''#%Module


    proc ModulesHelp { } {
    puts stderr "Defines the binary paths."
    puts stderr ""
    }

    conflict bmodule
    setenv AVAR myvalue
    prepend-path PATH /opt/software/B-1.0
    ''')
                with open(os.path.join(tempdir, 'bmodule', '1.1'), 'w') as bmod_f:
                    bmod_f.write('''#%Module


    proc ModulesHelp { } {
    puts stderr "Defines the binary paths."
    puts stderr ""
    }

    conflict bmodule
    setenv AVAR myvalue
    prepend-path PATH /opt/software/B-1.1
    ''')
                with patch.dict(
                        'fsl_sub.shell_modules.os.environ',
                        {'MODULEPATH': tempdir, }):
                    fsl_sub.shell_modules.get_modules.cache_clear()
                    self.assertEqual(
                        fsl_sub.shell_modules.get_modules('bmodule'),
                        ['1.0', '1.1']
                    )

    @unittest.skipUnless(LMOD, "Lmod not installed")
    def testLmodload(self):
        with tempfile.TemporaryDirectory() as tempdir:
            os.mkdir(os.path.join(tempdir, 'amodule'))
            with open(os.path.join(tempdir, 'amodule', '1.0'), 'w') as amod_f:
                amod_f.write('''#%Module


proc ModulesHelp { } {
puts stderr "Defines the binary paths."
puts stderr ""
}

conflict amodule
setenv AVAR myvalue
prepend-path PATH /opt/software/A
''')
            os.mkdir(os.path.join(tempdir, 'bmodule'))
            with open(os.path.join(tempdir, 'bmodule', '2.0.lua'), 'w') as bmod_f:
                bmod_f.write('''-- -*- lua -*-
help([[
For detailed instructions, go to:
   https://...

]])
whatis("Version: 2.0")
whatis("Keywords: System, Utility")
whatis("Description: Testing")

setenv(       "BVAR",        "anothervalue")
prepend_path( "PATH",           "/opt/software/B")
''')
            path = '/usr/bin:/usr/sbin:/sbin:/bin'
            os.environ['PATH'] = path
            os.chdir('/tmp')
            with patch.dict(
                    'fsl_sub.shell_modules.os.environ',
                    {'MODULEPATH': ':'.join((tempdir, os.environ['MODULEPATH']))}):
                with self.subTest('Test A'):
                    with patch('fsl_sub.shell_modules.update_environment', autospec=True) as mock_ue:
                        self.assertTrue(fsl_sub.shell_modules.load_module('amodule', testingLmod=True))
                        (name, positional, keyword) = mock_ue.mock_calls[0]
                        env_dict = positional[0]
                        self.assertTrue('AVAR' in env_dict['add'])
                        self.assertEqual(env_dict['add']['AVAR'], 'myvalue')
                        self.assertTrue('PATH' in env_dict['add'])
                        self.assertEqual(
                            env_dict['add']['PATH'],
                            ':'.join(('/opt/software/A', path))
                        )
                        self.assertListEqual(env_dict['remove'], [])

                with self.subTest('Test remove B'):
                    self.assertTrue(fsl_sub.shell_modules.load_module('bmodule', testingLmod=True))
                    with patch('fsl_sub.shell_modules.update_environment', autospec=True) as mock_ue:
                        self.assertTrue(fsl_sub.shell_modules.unload_module('bmodule', testingLmod=True))
                        (name, positional, keyword) = mock_ue.mock_calls[0]
                        env_dict = positional[0]
                        self.assertTrue('BVAR' in env_dict['remove'])
                        self.assertTrue('PATH' in env_dict['add'])
                        self.assertEqual(env_dict['add']['PATH'], path)

                    self.assertTrue(fsl_sub.shell_modules.unload_module('bmodule', testingLmod=True))


@unittest.skipUnless(CMOD, "Cmodules not installed")
class TestCmodulesSupport(unittest.TestCase):
    def setUp(self):
        os.chdir('/tmp')

    def testCmodGetModules(self):
        with tempfile.TemporaryDirectory() as tempdir:
            with open(os.path.join(tempdir, 'amodule'), 'w') as amod_f:
                amod_f.write('''#%Module


proc ModulesHelp { } {
puts stderr "Defines the binary paths."
puts stderr ""
}

conflict amodule
setenv AVAR myvalue
prepend-path PATH /opt/software/A
''')
            mcmd = shutil.which('modulecmd')
            lpath = ':'.join(('/usr/bin', os.path.dirname(mcmd)))
            with patch.dict(
                    'fsl_sub.shell_modules.os.environ',
                    {
                        'MODULEPATH': tempdir,
                        'PATH': lpath,
                    }):
                fsl_sub.shell_modules.get_modules.cache_clear()
                self.assertEqual(
                    fsl_sub.shell_modules.get_modules('amodule'),
                    ['amodule']
                )
            with self.subTest("Multiple versions"):
                os.mkdir(os.path.join(tempdir, 'bmodule'))
                with open(os.path.join(tempdir, 'bmodule', '1.0'), 'w') as bmod_f:
                    bmod_f.write('''#%Module


    proc ModulesHelp { } {
    puts stderr "Defines the binary paths."
    puts stderr ""
    }

    conflict bmodule
    setenv AVAR myvalue
    prepend-path PATH /opt/software/B-1.0
    ''')
                with open(os.path.join(tempdir, 'bmodule', '1.1'), 'w') as bmod_f:
                    bmod_f.write('''#%Module


    proc ModulesHelp { } {
    puts stderr "Defines the binary paths."
    puts stderr ""
    }

    conflict bmodule
    setenv AVAR myvalue
    prepend-path PATH /opt/software/B-1.1
    ''')
                mcmd = shutil.which('modulecmd')
                lpath = ':'.join(('/usr/bin', os.path.dirname(mcmd)))
                with patch.dict(
                        'fsl_sub.shell_modules.os.environ',
                        {
                            'MODULEPATH': tempdir,
                            'PATH': lpath,
                        }, clear=True):
                    fsl_sub.shell_modules.get_modules.cache_clear()
                    self.assertEqual(
                        fsl_sub.shell_modules.get_modules('bmodule'),
                        ['1.0', '1.1']
                    )

    @patch('fsl_sub.shell_modules.update_environment', autospec=True)
    def testCmodload(self, mock_ue):
        with tempfile.TemporaryDirectory() as tempdir:
            with open(os.path.join(tempdir, 'amodule'), 'w') as amod_f:
                amod_f.write('''#%Module


proc ModulesHelp { } {
puts stderr "Defines the binary paths."
puts stderr ""
}

conflict amodule
setenv AVAR myvalue
prepend-path PATH /opt/software/A
''')
            mcmd = shutil.which('modulecmd')
            os.chdir('/tmp')
            lpath = ':'.join(('/usr/bin', os.path.dirname(mcmd)))
            with self.subTest('Add A'):
                with patch.dict(
                        'fsl_sub.shell_modules.os.environ',
                        {
                            'MODULEPATH': tempdir,
                            'PATH': lpath,
                        }):
                    self.assertTrue(fsl_sub.shell_modules.load_module('amodule'))
                    (name, positional, keyword) = mock_ue.mock_calls[0]
                    env_dict = positional[0]
                    self.assertTrue('AVAR' in env_dict['add'])
                    self.assertEqual(env_dict['add']['AVAR'], 'myvalue')
                    self.assertTrue('PATH' in env_dict['add'])
                    self.assertEqual(
                        env_dict['add']['PATH'],
                        ':'.join(('/opt/software/A', lpath))
                    )
                    self.assertListEqual(env_dict['remove'], [])

            mock_ue.reset_mock()
            with self.subTest('Remove A'):
                with patch.dict(
                        'fsl_sub.shell_modules.os.environ',
                        {
                            'LOADEDMODULES': 'amodule',
                            '_LMFILES_': os.path.join(tempdir, 'amodule'),
                            'MODULEPATH': tempdir,
                            'AVAR': 'myvalue',
                            'PATH': ':'.join(('/opt/software/A', lpath)),
                        }):
                    self.assertTrue(fsl_sub.shell_modules.unload_module('amodule'))
                    (name, positional, keyword) = mock_ue.mock_calls[0]
                    env_dict = positional[0]
                    self.assertTrue('AVAR' in env_dict['add'])
                    self.assertEqual(env_dict['add']['AVAR'], '')
                    self.assertTrue('PATH' in env_dict['add'])
                    self.assertEqual(
                        env_dict['add']['PATH'],
                        lpath
                    )
                    self.assertListEqual(
                        sorted(env_dict['remove']),
                        sorted(['AVAR', 'LOADEDMODULES', '_LMFILES_']))

            mock_ue.reset_mock()
            with self.subTest('Remove A (2)'):
                with patch.dict(
                        'fsl_sub.shell_modules.os.environ',
                        {
                            'LOADEDMODULES': 'amodule:bmodule',
                            '_LMFILES_': ":".join((
                                os.path.join(tempdir, 'amodule'),
                                os.path.join(tempdir, 'bmodule'),
                            )),
                            'MODULEPATH': tempdir,
                            'AVAR': 'myvalue',
                            'PATH': ':'.join(('/opt/software/A', '/opt/software/B', lpath)),
                        },
                        clear=True):
                    self.assertTrue(fsl_sub.shell_modules.unload_module('amodule'))
                    (name, positional, keyword) = mock_ue.mock_calls[0]
                    env_dict = positional[0]
                    self.assertTrue('AVAR' in env_dict['add'])
                    self.assertEqual(env_dict['add']['AVAR'], '')
                    self.assertTrue('PATH' in env_dict['add'])
                    self.assertEqual(
                        env_dict['add']['PATH'],
                        ':'.join(('/opt/software/B', lpath))
                    )
                    self.assertListEqual(env_dict['remove'], ['AVAR'])


class TestModuleSupport(unittest.TestCase):
    def setUp(self):
        fsl_sub.shell_modules.get_modules.cache_clear()

    @patch('fsl_sub.shell_modules.shutil.which', autospec=True)
    def test_find_module_cmd(self, mock_which):
        mock_which.return_value = '/usr/bin/modulecmd'
        names_to_remove = {"LMOD_CMD"}
        modified_environ = {
            k: v for k, v in os.environ.items() if k not in names_to_remove
        }
        with patch.dict(fsl_sub.shell_modules.os.environ, modified_environ, clear=True):
            self.assertEqual(
                fsl_sub.shell_modules.find_module_cmd(),
                '/usr/bin/modulecmd')
            mock_which.assert_called_once_with('modulecmd')
            mock_which.reset_mock()
            with patch(
                    'fsl_sub.shell_modules.read_config',
                    return_value={'modulecmd': '/opt/bin/modulecmd', },
                    autospec=True):
                mock_which.return_value = '/opt/bin/modulecmd'
                self.assertEqual(
                    fsl_sub.shell_modules.find_module_cmd(),
                    '/opt/bin/modulecmd')
                mock_which.assert_not_called()
            mock_which.reset_mock()
            with patch(
                    'fsl_sub.shell_modules.read_config',
                    return_value={'modulecmd': '/usr/local/bin/modulecmd', },
                    autospec=True):
                mock_which.return_value = None
                self.assertEqual(
                    fsl_sub.shell_modules.find_module_cmd(),
                    '/usr/local/bin/modulecmd'
                )
            mock_which.reset_mock()
            with patch(
                    'fsl_sub.shell_modules.read_config',
                    return_value={'modulecmd': None, },
                    autospec=True):
                mock_which.return_value = None
                self.assertFalse(
                    fsl_sub.shell_modules.find_module_cmd()
                )

    def test_read_module_environment(self):
        lines = [
            "os.environ['PATH']='/usr/bin:/usr/sbin:/usr/local/bin'",
            "os.environ['LD_LIBRARY_PATH']='/usr/lib64:/usr/local/lib64'",
        ]
        self.assertDictEqual(
            fsl_sub.shell_modules.read_module_environment(lines),
            {
                'add': {
                    'PATH': '/usr/bin:/usr/sbin:/usr/local/bin',
                    'LD_LIBRARY_PATH': '/usr/lib64:/usr/local/lib64', },
                'remove': []
            }
        )

    @patch('fsl_sub.shell_modules.find_module_cmd', autospec=True)
    @patch('fsl_sub.shell_modules.system_stdout', autospec=True)
    @patch('fsl_sub.shell_modules.read_module_environment', autospec=True)
    def test_process_module(
            self,
            mock_read_module_environment,
            mock_system_stdout,
            mock_find_module_cmd):
        mcmd = '/usr/bin/modulecmd'
        mock_system_stdout.return_value = [
            "os.environ['PATH']='/usr/bin:/usr/sbin:/usr/local/bin'",
            "os.environ['LD_LIBRARY_PATH']='/usr/lib64:/usr/local/lib64'"
        ]
        mock_find_module_cmd.return_value = mcmd
        mock_read_module_environment.return_value = {
            'add': {
                'PATH': '/usr/bin:/usr/sbin:/usr/local/bin',
                'LD_LIBRARY_PATH': '/usr/lib64:/usr/local/lub64',
            },
            'remove': [],
        }
        os.chdir('/tmp')
        with self.subTest('Test 1'):
            self.assertDictEqual(
                fsl_sub.shell_modules.process_module('amodule'),
                {
                    'add': {
                        'PATH': '/usr/bin:/usr/sbin:/usr/local/bin',
                        'LD_LIBRARY_PATH': '/usr/lib64:/usr/local/lub64',
                    },
                    'remove': [],
                }
            )
            mock_find_module_cmd.assert_called_once_with()
            mock_read_module_environment.assert_called_once_with(
                [
                    "os.environ['PATH']='/usr/bin:/usr/sbin:/usr/local/bin'",
                    "os.environ['LD_LIBRARY_PATH']='/usr/lib64:/usr/local/lib64'"
                ]
            )
            mock_system_stdout.assert_called_once_with(
                ' '.join((mcmd, "python", "load", 'amodule',)), cwd=os.getcwd(), shell=True)
        with self.subTest('Test 1b'):
            mock_system_stdout.return_value = [
                "os.environ['PATH']='/usr/bin:/usr/sbin:/usr/local/bin'",
                "os.environ['LD_LIBRARY_PATH']='/usr/lib64:/usr/local/lib64'"
            ]
            mock_system_stdout.reset_mock()
            mock_find_module_cmd.reset_mock()
            mock_read_module_environment.reset_mock()
            self.assertDictEqual(
                fsl_sub.shell_modules.process_module('amodule'),
                {
                    'add': {
                        'PATH': '/usr/bin:/usr/sbin:/usr/local/bin',
                        'LD_LIBRARY_PATH': '/usr/lib64:/usr/local/lub64',
                    },
                    'remove': [],
                }
            )
            mock_find_module_cmd.assert_called_once_with()
            mock_read_module_environment.assert_called_once_with(
                [
                    "os.environ['PATH']='/usr/bin:/usr/sbin:/usr/local/bin'",
                    "os.environ['LD_LIBRARY_PATH']='/usr/lib64:/usr/local/lib64'"
                ]
            )
            mock_system_stdout.assert_called_once_with(
                " ".join((mcmd, "python", "load", 'amodule', )), cwd=os.getcwd(), shell=True)
        with self.subTest('Test 2'):
            mock_system_stdout.side_effect = subprocess.CalledProcessError(
                'acmd', 1)
            self.assertRaises(
                fsl_sub.shell_modules.LoadModuleError,
                fsl_sub.shell_modules.process_module,
                'amodule')

        with self.subTest('Test 3'):
            mock_find_module_cmd.return_value = ''
            self.assertFalse(
                fsl_sub.shell_modules.process_module('amodule')
            )

    @patch('fsl_sub.shell_modules.process_module', autospec=True)
    @patch.dict('fsl_sub.shell_modules.os.environ', {}, clear=True)
    def test_load_module(self, mock_process_module):
        mock_process_module.return_value = {
            'add': {'VAR': 'VAL', 'VAR2': 'VAL2', },
            'remove': [],
        }
        with self.subTest('Test 1'):
            self.assertTrue(
                fsl_sub.shell_modules.load_module('amodule'))
            self.assertDictEqual(
                dict(fsl_sub.shell_modules.os.environ),
                {'VAR': 'VAL', 'VAR2': 'VAL2', }
            )
        with self.subTest('Test 2'):
            mock_process_module.return_value = {}
            self.assertFalse(
                fsl_sub.shell_modules.load_module('amodule'))
        with self.subTest("Add to loadedmodules"):
            mock_process_module.return_value = {
                'add': {'LOADEDMODULES': 'bmodule/1.2.3', 'VAR': 'VAL', 'VAR2': 'VAL2', },
                'remove': []
            }
            self.assertTrue(
                fsl_sub.shell_modules.load_module('amodule'))
            self.assertDictEqual(
                dict(fsl_sub.shell_modules.os.environ),
                {'LOADEDMODULES': 'bmodule/1.2.3', 'VAR': 'VAL', 'VAR2': 'VAL2', }
            )

    @patch('fsl_sub.shell_modules.process_module', autospec=True)
    def test_load_module2(self, mock_process_module):
        with self.subTest("Add to loadedmodules 2"):
            with patch.dict('fsl_sub.shell_modules.os.environ', {'LOADEDMODULES': 'amodule/2.3.4', }, clear=True):
                mock_process_module.return_value = {
                    'add': {'LOADEDMODULES': 'amodule/2.3.4:bmodule/1.2.3', 'VAR': 'VAL', 'VAR2': 'VAL2', },
                    'remove': []
                }
                self.assertTrue(
                    fsl_sub.shell_modules.load_module('bmodule'))
                self.assertDictEqual(
                    dict(fsl_sub.shell_modules.os.environ),
                    {'LOADEDMODULES': 'amodule/2.3.4:bmodule/1.2.3', 'VAR': 'VAL', 'VAR2': 'VAL2', }
                )

    @patch('fsl_sub.shell_modules.process_module', autospec=True)
    def test_unload_module(self, mock_process_module):
        with self.subTest("Unload modules"):
            with patch.dict(
                    'fsl_sub.shell_modules.os.environ', {
                        'LOADEDMODULES': 'bmodule/1.2.3:amodule/2.3.4:', 'VAR': 'VAL', 'VAR2': 'VAL2', },
                    clear=True):
                mock_process_module.return_value = {
                    'add': {'LOADEDMODULES': 'bmodule/1.2.3', },
                    'remove': ['VAR', 'VAR2', ],
                }
                self.assertTrue(
                    fsl_sub.shell_modules.unload_module('amodule'))
                self.assertDictEqual(
                    dict(fsl_sub.shell_modules.os.environ),
                    {'LOADEDMODULES': 'bmodule/1.2.3', }
                )

    @patch.dict(
        'fsl_sub.shell_modules.os.environ',
        {'LOADEDMODULES': 'mod1:mod2:mod3', 'EXISTING': 'VALUE', },
        clear=True)
    def test_loaded_modules(self):
        with self.subTest('Test 1'):
            self.assertListEqual(
                fsl_sub.shell_modules.loaded_modules(),
                ['mod1', 'mod2', 'mod3', ])
        with self.subTest('Test 2'):
            with patch.dict(
                    'fsl_sub.shell_modules.os.environ',
                    {'EXISTING': 'VALUE', },
                    clear=True):
                self.assertListEqual(
                    fsl_sub.shell_modules.loaded_modules(),
                    [])

    @patch('fsl_sub.shell_modules.system_stderr', autospec=True)
    @patch('fsl_sub.shell_modules.find_module_cmd', autospec=True)
    def test_get_modules(self, mock_fmc, mock_system_stderr):
        mock_system_stderr.return_value = [
            "/usr/local/etc/ShellModules:",
            "amodule/5.0",
            "amodule/5.5",
            "/usr/share/Modules/modulefiles:",
            "/etc/modulefiles:",
        ]
        mock_fmc.return_value = '/usr/bin/modulecmd'
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Test 1'):
            self.assertListEqual(
                fsl_sub.shell_modules.get_modules('amodule'),
                ['5.0', '5.5', ])
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Test 1b'):
            mock_system_stderr.reset_mock()
            mock_system_stderr.return_value = [
                "/usr/local/etc/ShellModules:",
                "bmodule",
            ]
            self.assertListEqual(
                fsl_sub.shell_modules.get_modules('bmodule'),
                ['bmodule', ])
        mock_system_stderr.reset_mock()
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Module parent with /'):
            mock_system_stderr.reset_mock()
            mock_system_stderr.return_value = [
                "/usr/local/etc/ShellModules:",
                "bmodule/submodule/version",
            ]
            self.assertListEqual(
                fsl_sub.shell_modules.get_modules('bmodule/submodule'),
                ['version', ]
            )
        mock_system_stderr.reset_mock()
        mock_system_stderr.return_value = ''
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Test long lines'):
            mock_system_stderr.return_value = [
                '''------------------------------------------'''
                + '''--------------------------------------------- '''
                + '''/apps/system/easybuild/modules/all'''
                + ''' ---------------------------------------------'''
                + '''-------------------------------------------''',
                '''   Amodule/1.2.3                              '''
                + '''                         Amodule/2.14         '''
                + '''                          Amodule/7.3.0''',
                '''   Amodule/2.1.5                              '''
                + '''                         Amodule/2.13.03      '''
                + '''                          Amodule/2.13.1''']
            self.assertListEqual(
                fsl_sub.shell_modules.get_modules('Amodule'),
                ['1.2.3', '2.1.5', '2.13.03', '2.13.1', '2.14', '7.3.0', ]
            )
        mock_system_stderr.reset_mock()
        mock_system_stderr.return_value = ''
        fsl_sub.shell_modules.get_modules.cache_clear()

        with self.subTest('Test module parent within name'):
            mock_system_stderr.return_value = [
                'Amodule/1.2.3',
                'Bmodule/3.2.1',
                'Cmodule-Amodule-Bmodule/2.3.4',
                'Cmodule-Amodule/3.4.5']
            self.assertListEqual(
                fsl_sub.shell_modules.get_modules('Amodule'),
                ['1.2.3']
            )
        mock_system_stderr.reset_mock()
        mock_system_stderr.return_value = ''
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Test module parent within name 2'):
            mock_system_stderr.return_value = [
                'Amodule/1.2.3',
                'AmoduleA/3.2.1', ]
            self.assertListEqual(
                fsl_sub.shell_modules.get_modules('Amodule'),
                ['1.2.3']
            )
        mock_system_stderr.reset_mock()
        mock_system_stderr.return_value = ''
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Test module parent within name 3'):
            mock_system_stderr.return_value = [
                'Amodule/1.2.3',
                'Amodule-3.2.1',
                'Amodule/submodule/4.3.2',
                'Amodulesubmodule/5.4.3',
            ]
            self.assertListEqual(
                fsl_sub.shell_modules.get_modules('Amodule'),
                ['1.2.3', '4.3.2', ]
            )
        mock_system_stderr.reset_mock()
        mock_system_stderr.return_value = [
            "/usr/local/etc/ShellModules:",
            "amodule/",
            "amodule/5.5",
        ]
        mock_fmc.return_value = '/usr/bin/modulecmd'
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Test Lmod reporting parent separately'):
            self.assertListEqual(
                fsl_sub.shell_modules.get_modules('amodule'),
                ['5.5', ])
        mock_system_stderr.reset_mock()
        mock_system_stderr.return_value = ''
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Test 2'):
            mock_system_stderr.side_effect = subprocess.CalledProcessError(
                'acmd', 1
            )
            self.assertRaises(
                fsl_sub.shell_modules.NoModule,
                fsl_sub.shell_modules.get_modules, 'amodule')
        mock_system_stderr.reset_mock()
        mock_system_stderr.return_value = ''
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Test 3'):
            self.assertRaises(
                fsl_sub.shell_modules.NoModule,
                fsl_sub.shell_modules.get_modules, 'amodule')

    @patch('fsl_sub.shell_modules.get_modules', autospec=True)
    def test_latest_module(self, mock_get_modules):
        with self.subTest('Test 1'):
            mock_get_modules.return_value = ['5.0', '5.5', ]
            self.assertEqual(
                fsl_sub.shell_modules.latest_module('amodule'),
                '5.5')
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Test 2'):
            mock_get_modules.return_value = None
            self.assertFalse(
                fsl_sub.shell_modules.latest_module('amodule')
            )
        fsl_sub.shell_modules.get_modules.cache_clear()
        with self.subTest('Test 3'):
            mock_get_modules.side_effect = fsl_sub.shell_modules.NoModule(
                'amodule')
            self.assertRaises(
                fsl_sub.shell_modules.NoModule,
                fsl_sub.shell_modules.latest_module, 'amodule'
            )

    def test_module_string(self):
        with self.subTest('Test 1'):
            self.assertEqual(
                fsl_sub.shell_modules.module_string('amodule', '5.0'),
                'amodule/5.0'
            )
        with self.subTest('Test 2'):
            self.assertEqual(
                fsl_sub.shell_modules.module_string('amodule', None),
                'amodule'
            )


if __name__ == '__main__':
    unittest.main()
