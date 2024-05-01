import logging.config

from src.utils.logging_filter import RequestIdFilter

from .config import config

LOGGING_CONFIG = {
    'version': 1,
    'filters': {
        'request_id': {
            '()': RequestIdFilter,
        },
    },
    'formatters': {
        'default': {
            'format': '%(levelname)s::%(asctime)s:%(name)s.%(funcName)s:%(request_id)s\n%(message)s\n',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': config.LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
            'filters': ['request_id'],
        },
    },
    'loggers': {
        config.APP_NAME: {
            'level': config.LOG_LEVEL,
            'handlers': (['console', ]),
        },
    },
    'disable_existing_loggers': False,
}


def init_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
