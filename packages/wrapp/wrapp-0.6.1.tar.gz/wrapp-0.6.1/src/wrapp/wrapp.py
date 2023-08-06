#!/usr/bin/env python3
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from logging import getLogger, Logger, StreamHandler, Formatter
from pathlib import Path
from importlib import import_module
import logging
import sys


LOG = getLogger(__name__)

LOG_LEVEL = logging.INFO

_TEMPLATE = '''#!/usr/bin/env python3
from logging import getLogger


LOG = getLogger(__name__)


def set_logger(parent_name):
    global LOG
    LOG = getLogger(f'{parent_name}.{__name__}')


def add_arguments(parser):
    group = parser.add_argument_group(__name__)
    ...


def main(args):
    ...


# code below is an option.
# if you want to run it as an normal Python script
# (`python THIS_SCRIPT.py`), uncomment it.
# if __name__ == '__main__':
#     import wrapp
#     wrapp.main(add_arguments, main, set_logger)'''


def _import_module():
    if len(sys.argv) == 1 or sys.argv[1] in ('-h', '--help'):
        argv0 = Path(sys.argv[0]).name
        ArgumentParser(
                usage=f'{argv0} MODULE_OR_SCRIPT ..',
                ).print_help()
        exit()
    sys.path.insert(0, str(Path(sys.argv[0]).cwd()))
    args = sys.argv[1:]
    argv0_path = Path(args[0])
    if len(argv0_path.parts) > 1:
        sys.path.append(str(argv0_path.parent))
    module_name = Path(argv0_path.name).stem
    module = import_module(module_name)
    assert hasattr(module, 'main'), (
            f'{module_name} does not have main()')
    assert hasattr(module, 'add_arguments'), (
            f'{module_name} does not have add_arguments()')
    return module


def _parse_module_arguments(module):
    parser = ArgumentParser(
            prog=sys.argv[1],
            formatter_class=ArgumentDefaultsHelpFormatter)
    module.add_arguments(parser)
    args = parser.parse_args(sys.argv[2:])
    return args


def _set_logger(logger, level):
    if not isinstance(logger, Logger):
        LOG.warning((
            f'type of logger = {type(logger)} is not logging.Logger.'
            ' do nothing.'))
        return
    __handler = StreamHandler()
    __handler.setLevel(level)
    __handler.setFormatter(Formatter(
        '%(levelname).1s %(asctime)s %(filename)s:%(lineno)d %(message)s'
    ))
    logger.setLevel(level)
    logger.addHandler(__handler)


def _print_args(args):
    for k, v in vars(args).items():
        LOG.info(f'{k}= {v}')


def _parse_args(add_arguments_func):
    parser = ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter)
    add_arguments_func(parser)
    args = parser.parse_args()
    return args


def app():
    '''
    comes here when wrapp YOUR_SCRIPT ... is run.
    '''
    module = _import_module()
    _set_logger(LOG, LOG_LEVEL)
    if hasattr(module, 'set_logger'):
        module.set_logger(LOG.name)
    args = _parse_module_arguments(module)
    _print_args(args)
    module.main(args)


def new():
    '''
    comes here when wrapp.new is run.
    '''
    print(_TEMPLATE, end='')


def main(add_arguments_func, main_func, set_logger_func):
    '''
    use this function when you want to use usual if __name__ == '__main__': block.
    '''
    set_logger_func(LOG.name)
    _set_logger(LOG, LOG_LEVEL)
    args = _parse_args(add_arguments_func)
    _print_args(args)
    main_func(args)


if __name__ == '__main__':
    app()
