# fsl_sub python module
# Copyright (c) 2018-2021 University of Oxford (Duncan Mortimer)

from fsl_sub.config import (
    method_config,
    queue_config,
    read_config,
)
from fsl_sub.exceptions import (
    ArgumentError,
)


def has_parallel_envs(config=None):
    '''Return True if the plugin supports parallel environments'''
    if config is None:
        config = read_config()
    mconf = method_config(config['method'], config)

    result = False

    if 'has_parallel_envs' in mconf:
        result = mconf['has_parallel_envs']
    elif mconf.get('queues', False):
        # Method uses queues
        result = True if parallel_envs(config['queues']) is not None else False

    return result


def parallel_envs(queues=None):
    '''Return the list of configured parallel environments
    in the supplied queue definition dict'''
    if queues is None:
        queues = queue_config()
    ll_envs = []
    for q in queues.values():
        try:
            ll_envs.extend(q.get('parallel_envs', []))
        except KeyError:
            pass
    if not ll_envs:
        return None
    return list(set(ll_envs))


def process_pe_def(pe_def, queues):
    '''Convert specified pe,slots into a tuples'''
    pes_defined = parallel_envs(queues)
    try:
        pe = pe_def.split(',')
    except ValueError:
        raise ArgumentError(
            "Parallel environment must be name,slots"
        )

    if has_parallel_envs():
        if pes_defined:
            if pe[0] not in pes_defined:
                raise ArgumentError(
                    "Parallel environment name {} "
                    "not recognised".format(pe[0])
                )
            pe_name = pe[0]
            slots = pe[1]
        else:
            raise ArgumentError("No parallel environments defined")
    else:
        slots = pe[-1]
        pe_name = None
    try:
        slots = int(slots)
    except ValueError:
        raise ArgumentError(
            "Slots requested not an integer"
        )
    return (pe_name, slots, )
