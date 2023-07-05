import os, sys
from config import today

if not os.path.exists("./Logs/error/" + today + "_error.log"):
    open("./Logs/error/" + today + "_error.log", 'a').close()

LOGGING_CONFIG = {
    'version': 1, 
    'disable_existing_loggers': False, 
    'loggers': {
        'sanic.root': {
            'level': 'INFO', 
            'handlers': ['console', 'file']
        }, 
        'sanic.error': {
            'level': 'INFO', 
            'handlers': ['error_console', 'error_file'], 
            'propagate': True, 
            'qualname': 'sanic.error'
        }
    }, 
    'formatters': {
        'generic': {
            'format': '%(asctime)s [%(process)s] [%(levelname)s] %(message)s', 
            'datefmt': '[%Y-%m-%d %H:%M:%S %z]', 
            'class': "logging.Formatter"
        }, 
        'access': {
            'format': '%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: %(request)s %(message)s %(status)s %(byte)s', 
            'datefmt': '[%Y-%m-%d %H:%M:%S %z]', 
            'class': "logging.Formatter"
        }, 
        'generic_json': {
            'format': '%(asctime)s %(process)s %(levelname)s %(message)s', 
            'datefmt': '[%Y-%m-%d %H:%M:%S %z]', 
            'class': "pythonjsonlogger.jsonlogger.JsonFormatter"
        }
    }, 
    'handlers': {
        'console': {
            'class': "logging.StreamHandler", 
            'formatter': 'generic', 
            'stream': sys.stdout
        }, 
        'error_console': {
            'class': "logging.StreamHandler", 
            'formatter': 'generic', 
            'stream': sys.stderr
        },
        'file': {
            'class': 'logging.FileHandler', 
            'formatter': 'generic_json', 
            'filename': "./Logs/" + today + ".log"
        },
        'error_file': {
            'class': 'logging.FileHandler', 
            'formatter': 'generic_json', 
            'level': 'ERROR', 
            'filename': "./Logs/error/" + today + "_error.log"
        }
    }
}
