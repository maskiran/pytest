import datetime
import inspect
import logging
import os
import pytest
from types import SimpleNamespace


def print_obj(obj):
    for key in dir(obj):
        if key.startswith('_'):
            continue
        print(key, getattr(obj, key))


@pytest.fixture(scope="session")
def setup_session():
    print("####At session")
    logdir = os.path.join('logs',
                          datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return {
        'session_logdir': logdir,
        'logger': logger
    }


@pytest.fixture(scope="function")
def tc(request, setup_session):
    tc_obj = prepare_tc(request, setup_session)
    logger = tc_obj.logger
    logger.info('Setting up to run test %s', request.node.name)
    yield tc_obj
    logger.info('Cleaning up to run test %s', request.node.name)


def prepare_tc(request, setup_session):
    session_logdir = setup_session['session_logdir']
    module_name = inspect.getmodulename(request.fspath)
    module_log_dir = os.path.join(session_logdir, module_name)
    logger = setup_session['logger']
    os.makedirs(module_log_dir, exist_ok=True)
    log_file = os.path.join(module_log_dir, request.node.name)
    for h in logger.handlers:
        logger.removeHandler(h)
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)s %(message)s",
        datefmt="%Y-%m-%d-%H:%M:%S")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return SimpleNamespace(
        function=request.node,
        logger=logger,
        log_dir=module_log_dir,
        log_file=log_file,
    )
