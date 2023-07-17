from core.configs import LogConfig

log_config = LogConfig()

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': log_config.CONSOLE_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': log_config.UVICORN_LOG_LEVEL,
        },
        'uvicorn.error': {
            'level': log_config.UVICORN_LOG_LEVEL,
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': log_config.UVICORN_LOG_LEVEL,
            'propagate': False,
        },
    },
    'root': {
        'level': log_config.ROOT_LOG_LEVEL,
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
