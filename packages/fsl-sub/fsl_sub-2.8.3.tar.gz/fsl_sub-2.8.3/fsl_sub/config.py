# fsl_sub python module
# Copyright (c) 2018-2021 University of Oxford (Duncan Mortimer)

import logging
import os
import os.path
from shutil import which
import subprocess as sp
import warnings
from ruamel.yaml import (YAML, YAMLError, )

from fsl_sub.exceptions import (BadConfiguration, MissingConfiguration, )
from fsl_sub.utils import (
    get_plugin_default_conf,
    get_plugin_queue_defs,
    get_plugin_already_queued,
    available_plugins,
    merge_dict,
    merge_commentedmap,
    plugins_provide_coproc,
)
from functools import lru_cache


def find_config_file():
    # Find most appropriate config file
    search_path = []
    try:
        env_config = os.environ['FSLSUB_CONF']
        search_path.append(env_config)
    except KeyError:
        pass

    search_path.append(
        os.path.join(
            os.path.expanduser("~"),
            '.fsl_sub.yml')
    )

    try:
        fsl_dir = os.environ['FSLDIR']
        default_conf = os.path.realpath(
            os.path.join(fsl_dir, 'etc', 'fslconf', 'fsl_sub.yml')
        )
        search_path.append(
            os.path.abspath(default_conf)
        )
    except KeyError:
        pass
    search_path.append(
        os.path.abspath(
            os.path.join(
                os.path.realpath(__file__),
                os.path.pardir,
                'plugins',
                'fsl_sub_shell.yml')))

    for p in search_path:
        if os.path.exists(p) and os.path.getsize(p) > 0:
            return p

    raise MissingConfiguration("Unable to find fsl_sub config")


def _internal_config_file(filename):
    return os.path.join(os.path.realpath(os.path.dirname(__file__)), filename)


def load_default_config():
    dc_file = _internal_config_file("default_config.yml")
    dcc_file = _internal_config_file("default_coproc_config.yml")
    default_config = {}
    yaml = YAML(typ='safe')
    for d_conf_f in (dc_file, dcc_file, ):
        try:
            with open(d_conf_f, 'r') as yaml_source:
                yc = yaml.load(yaml_source)
                default_config = merge_dict(default_config, yc)
        except YAMLError as e:
            raise BadConfiguration(
                "Unable to understand default configuration: " + str(e))
        except FileNotFoundError:
            raise MissingConfiguration(
                "Unable to find default configuration file: " + d_conf_f)
        except PermissionError:
            raise MissingConfiguration(
                "Unable to open default configuration file: " + d_conf_f)

    for plugin in available_plugins():
        try:
            plugin_yaml = get_plugin_default_conf(plugin)
            p_dc = yaml.load(plugin_yaml)
        except Exception as e:
            raise BadConfiguration(
                "Unable to understand plugin "
                "{0}'s default configuration: ".format(plugin) + str(e))

        default_config = merge_dict(default_config, p_dc)

    default_config['method'] = 'shell'
    return default_config


@lru_cache()
def read_config():
    logger = logging.getLogger(__name__)

    yaml = YAML(typ='safe')
    default_config = load_default_config()
    try:
        config_file = find_config_file()
        logger.debug("Using {0} as config file".format(config_file))
        with open(config_file, 'r') as yaml_source:
            config_dict = yaml.load(yaml_source)
    except IsADirectoryError:
        raise BadConfiguration(
            "Unable to open configuration file - "
            "looks like FSLSUB_CONF may be pointing at a directory? " + config_file)
    except YAMLError as e:
        raise BadConfiguration(
            "Unable to understand configuration file: " + str(e))
    except (FileNotFoundError, PermissionError, ):
        raise BadConfiguration(
            "Unable to open configuration file: " + config_file
        )
    except MissingConfiguration:
        config_dict = {}
    base_config = merge_dict(default_config, config_dict)

    # Merge in the user's configuration
    user_config_file = os.path.join(os.path.expanduser("~"), '.fsl_sub.yml')
    if config_file != user_config_file and os.path.exists(user_config_file):
        try:
            with open(user_config_file, 'r') as yaml_source:
                user_config = yaml.load(yaml_source)
                if user_config is not None:
                    logger.debug("Merging in {0}".format(user_config_file))
                    final_config = merge_dict(base_config, user_config)
                else:
                    warnings.warn("{0} appears to be empty".format(user_config_file))
                    final_config = base_config
        except IsADirectoryError:
            raise BadConfiguration(
                "Unable to open configuration file - "
                "looks like ~/.fsl_sub.yml may be pointing at a directory? " + config_file)
        except YAMLError as e:
            raise BadConfiguration(
                "Unable to understand configuration file: " + str(e))
        except (FileNotFoundError, PermissionError, ):
            final_config = base_config
    else:
        final_config = base_config
    if config_dict.get('coproc_opts', {}):
        if 'cuda' not in config_dict['coproc_opts'].keys():
            if 'cuda' not in config_dict.get('silence_warnings', []):
                warnings.warn(
                    '(cuda) Coprocessors configured but no "cuda" coprocessor found. '
                    'FSL tools will not be able to autoselect CUDA versions of software.')
    return final_config


def method_config(method, config=None):
    '''Returns the configuration dict for the requested submission
    method, e.g. sge'''
    if config is None:
        config = read_config()
    try:
        m_opts = config['method_opts']
    except KeyError:
        raise BadConfiguration(
            "Unable to find method configuration dictionary"
        )
    try:
        return m_opts[method]
    except KeyError:
        raise BadConfiguration(
            "Unable to find configuration for {}".format(method)
        )


def _read_config_file(fname):
    '''Return content of file as string'''
    try:
        with open(fname, 'r') as default_source:
            e_conf = default_source.read().strip()
    except FileNotFoundError:
        raise MissingConfiguration(
            "Unable to find default configuration file: " + fname
        )
    return e_conf


def _read_rt_yaml_file(filename):
    yaml = YAML()
    with open(filename, 'r') as fh:
        return yaml.load(fh)


def _dict_from_yaml_string(ystr):
    yaml = YAML()
    return yaml.load(ystr)


def example_config(method=None):
    '''Merges the method default config output with the general defaults and returns
    the example config as a ruamel.yaml CommentedMap'''
    methods = ['shell', ]
    if method is None:
        method = 'shell'
    if method != 'shell':
        methods.append(method)

    e_conf = ''

    # Example config files
    cfs = {
        'dc': _read_rt_yaml_file(_internal_config_file("default_config.yml")),
        'dcc': _read_rt_yaml_file(_internal_config_file("default_coproc_config.yml")),
        'qc': _read_rt_yaml_file(_internal_config_file("example_queue_config.yml")),
        'cc': _read_rt_yaml_file(_internal_config_file("example_coproc_config.yml")),
    }

    e_conf = cfs['dc']
    if not plugins_provide_coproc(methods):
        e_conf = merge_commentedmap(e_conf, cfs['dcc'])

    # Add the method opts for the methods ('shell' + value of method)
    for m in methods:
        plugin_conf = get_plugin_default_conf(m)
        e_conf = merge_commentedmap(e_conf, _dict_from_yaml_string(plugin_conf))

    if method is not None:
        e_conf = merge_commentedmap(e_conf, cfs['cc'])
        # Try to detect queues
        queue_defs = get_plugin_queue_defs(method)
        if queue_defs:
            merge_in = queue_defs
        else:
            # Add the example queue config
            merge_in = cfs['qc']
        e_conf = merge_commentedmap(e_conf, merge_in)
    e_conf['method'] = method
    return e_conf


def has_queues(method=None):
    '''Returns True if method has queues and there are queues defined'''
    config = read_config()
    if method is None:
        method = config['method']
    mconf = method_config(method)
    return mconf['queues'] and config['queues']


def has_coprocessor(coproc):
    '''Is the specified coprocessor available on this system?'''
    config = read_config()
    method = config['method']
    queues = config.get('queues', {})
    coprocs = config.get('coproc_opts', {})
    if get_plugin_already_queued(method):
        method = 'shell'
    if method == 'shell':
        co_conf = coprocs.get(coproc, None)
        if co_conf is not None:
            tester = which(co_conf['presence_test'])
            if tester is None:
                return False
            else:
                output = sp.run(
                    [tester, ]
                )
                if output.returncode != 0:
                    return False
            return True
        else:
            # Unsupported coprocessor
            return False
    if queues:
        return any([(coproc in a.get('copros', {}).keys()) for qname, a in queues.items()])
    else:
        raise BadConfiguration("Grid backend specified but no queues configured")


def uses_projects(method=None):
    '''Returns True if method has projects'''
    if method is None:
        method = read_config()['method']
    m_config = method_config(method)
    return m_config['projects']


def coprocessor_config(coprocessor):
    '''Returns the configuration dict for the requested coprocessor,
    e.g. cuda'''
    try:
        cp_opts = read_config()['coproc_opts']
    except KeyError:
        raise BadConfiguration(
            "Unable to find coprocessor configuration dictionary"
        )
    try:
        return cp_opts[coprocessor]
    except KeyError:
        raise BadConfiguration(
            "Unable to find configuration for {}".format(coprocessor)
        )


def queue_config(queue=None):
    '''Returns the config dict for all queues or the config dict
    for the specified queue'''
    try:
        if queue is None:
            return read_config()['queues']
        else:
            return read_config()['queues'][queue]
    except KeyError:
        if queue is None:
            raise BadConfiguration(
                "Unable to find queue definitions"
            )
        else:
            raise BadConfiguration(
                "Unable to find definition for queue " + queue
            )


def validate_config(config):
    '''Basic sanity check of configuration'''

    logger = logging.getLogger(__name__)
    logger.debug("Validating config {0}".format(str(config)))
    method_opts = config['method_opts'][config['method']]

    errors = []
    # Check module command settings
    modulecmd = config.get('modulecmd', False)
    if modulecmd:
        if not os.path.isfile(modulecmd) or not os.access(modulecmd, os.X_OK):
            errors.append(
                "modulecmd is set to {0}, but this either does not exist or is"
                " not an executable".format(modulecmd))

    if method_opts.get('queues', False):
        queues = config.get('queues', [])
        logger.debug("Checking for empty queue definitions")
        for q, qc in queues.items():
            if qc is None:
                errors.append(
                    "Queue {0} has no configuration".format(q)
                )

        logger.debug("Checking for RAM split/PE configuration")

        split_pe = method_opts.get('large_job_split_pe', None)
        logger.debug("large_job_split_pe set to {0}".format(str(split_pe)))
        for q, qc in queues.items():
            if qc.get('map_ram', False):
                if 'parallel_envs' not in qc:
                    errors.append(
                        "Queue {0} has map_ram set to True but no parallel environments"
                        " listed".format(q))
                else:
                    if split_pe is None:
                        errors.append(
                            "Queue {0} has map_ram set to True but large_job_split_pe is not set".format(q))
                    else:
                        if split_pe not in qc.get('parallel_envs', []):
                            errors.append(
                                "{0} not found in configured parallel environments for {1}".format(split_pe, q))

        # Test for has_parallel_envs
        ll_envs = []
        for qd in config['queues'].values():
            if 'parallel_envs' in qd:
                ll_envs.append(True)
            else:
                ll_envs.append(False)

        if 'has_parallel_envs' not in method_opts:
            if any(ll_envs):
                warnings.warn(
                    "Configuration should be updated, queues have parallel environments defined"
                    " but method options for {0} is missing has_parallel_envs: true".format(
                        config['method']
                    ))
        elif method_opts['has_parallel_envs']:
            if not any(ll_envs):
                errors.append(
                    "Method options for {0} specifies has_parallel_envs: true but"
                    " no queues have parallel environments defined".format(
                        config['method']
                    )
                )

    if errors:
        raise BadConfiguration("\n".join(errors))
