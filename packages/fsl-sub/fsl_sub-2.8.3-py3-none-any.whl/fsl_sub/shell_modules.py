# fsl_sub python module
# Copyright (c) 2018-2021 University of Oxford (Duncan Mortimer)

import os
import re
import shlex
import shutil
import subprocess
from functools import lru_cache

from fsl_sub.exceptions import (
    LoadModuleError,
    NoModule,
)
from fsl_sub.config import (
    read_config,
)
from fsl_sub.system import system_stdout, system_stderr


def find_module_cmd():
    '''Locate the 'module' binary'''
    config = read_config()
    if config['modulecmd']:
        return config['modulecmd']

    # Identify the command:
    if 'LMOD_CMD' in os.environ:
        # Lmod
        return os.environ['LMOD_CMD']

    # Not Lmod - search for 'modulecmd'
    mcmd = shutil.which('modulecmd')
    return mcmd


def read_module_environment(lines):
    '''Given output of modulecmd python add ... convert this to a dict'''
    module_env = {'add': {}, 'remove': []}
    regex_add = re.compile(
        r"os.environ\[['\"](?P<variable>.*)['\"]\] ?= ?['\"](?P<value>.*)['\"];?$")
    regex_remove = re.compile(
        r"del os.environ\[['\"](?P<variable>.*)['\"]\];?$"
    )
    for line in lines:
        matches = regex_add.match(line.strip())
        if matches:
            module_env['add'][matches.group('variable')] = matches.group('value')
        matches = regex_remove.match(line.strip())
        if matches:
            module_env['remove'].append(matches.group('variable'))
    return module_env


def process_module(module_name, action='load', testingLmod=False):
    '''Returns a dict of variable: value describing the environment variables
    necessary to load a shell module into the current environment'''
    module_cmd = find_module_cmd()

    if module_cmd:
        cmd = [module_cmd, "python"]
        if testingLmod:
            cmd.append('--ignore-cache')
        cmd.extend((shlex.quote(action), shlex.quote(module_name)))
        try:
            environment = system_stdout(
                ' '.join(cmd),
                cwd=os.getcwd(),
                shell=True)
        except subprocess.CalledProcessError as e:
            raise LoadModuleError from e
        return read_module_environment(environment)
    else:
        return False


def update_environment(changes):
    '''Update the environment given a dict of 'add' variable:value or 'remove' list'''
    for k, v in changes['add'].items():
        os.environ[k] = v
    for k in changes['remove']:
        del os.environ[k]


def load_module(module_name, testingLmod=False):
    '''Load a module into the environment of this python process.'''
    environment = process_module(module_name, testingLmod=testingLmod)
    if environment:
        update_environment(environment)
        return True
    else:
        return False


def unload_module(module_name, testingLmod=False):
    '''Remove environment variables associated with module module_name
     from the environment of python process.'''
    environment = process_module(module_name, action='unload', testingLmod=testingLmod)
    if environment:
        update_environment(environment)
        return True
    else:
        return False


def loaded_modules():
    '''Get list of loaded ShellModules'''
    # Modules stored in environment variable LOADEDMODULES
    try:
        modules_string = os.environ['LOADEDMODULES']
    except KeyError:
        return []
    if modules_string == '':
        return []
    return modules_string.split(':')


@lru_cache()
def get_modules(module_parent):
    '''Returns a list of available Shell Modules that setup the
    co-processor environment'''
    modules = []
    module_cmd = find_module_cmd()
    if module_cmd is not None:
        try:
            available_modules = system_stderr(
                module_cmd + " bash -t avail " + shlex.quote(module_parent),
                shell=True)
            if available_modules:
                # Module output is tabulated
                lmods = []
                for line in available_modules:
                    line = line.strip()
                    lmods.extend(line.split())
                for item in lmods:
                    if not item:
                        continue
                    if ':' in item:
                        continue
                    if item == module_parent:
                        modules.append(item)
                    elif item.startswith(module_parent + '/'):
                        if item.endswith('/'):
                            continue  # Lmod will report the parent folder of versioned module files
                        else:
                            modules.append(item.split('/')[-1])
            else:
                raise NoModule(module_parent)
        except subprocess.CalledProcessError as e:
            if (
                    e.stderr is not None and 'Unable to locate' in e.stderr
                    or e.stdout is not None and 'The following module(s) are unknown' in e.stdout):
                raise NoModule(module_parent)
            else:
                raise NoModule(
                    "Error calling module command: stdout={0}; stderr={1}".format(e.stdout, e.stderr))
    else:
        modules = []
    return sorted(modules)


def latest_module(module_parent):
    '''Return the module string that would load the latest version of a module.
    Returns False if module is determined to be not versioned and raises
    NoModule if module is not found.'''
    try:
        modules = get_modules(module_parent)
        if modules is None:
            return False
        else:
            return modules[-1]
    except NoModule:
        raise


def module_string(module_parent, module_version):
    if module_version:
        return "/".join((module_parent, module_version))
    else:
        return module_parent
