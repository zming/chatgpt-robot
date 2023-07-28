import os
import sys
from conf import CONF

log_level = 'DEBUG' if CONF.DEBUG else 'INFO'

# Sanic 默认日志格式
# from sanic.log import LOGGING_CONFIG_DEFAULTS

# 没有日志目录，则创建日志目录
if not os.path.exists(os.path.dirname(CONF.LOG_FILE)):
    os.makedirs(os.path.dirname(CONF.LOG_FILE))

LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            "class": "logging.StreamHandler",
            'level': log_level,
            "formatter": "generic",
            "stream": sys.stdout,
        },
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': log_level,
            'formatter': 'debug',
            'filename': os.path.join(CONF.BASE_DIR, CONF.LOG_FILE),
            'maxBytes': 1024 * 1024 * 200,
            'backupCount': CONF.LOG_REMAIN,
            'encoding': 'utf-8'
        },
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s:%(lineno)d | %(message)s',
        },
        'debug': {
            'format': '%(asctime)s - %(levelname)s - %(name)s:%(lineno)d | %(message)s',
        },
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
                      + "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'logfile'],
            'propagate': True
        },
    }
}