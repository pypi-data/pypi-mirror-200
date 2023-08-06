
def get_logging_config(log_file):
    LOGGING_CONFIG = {
		'version': 1,
        'loggers': {
            '': { # root logger
                'level': 'INFO',
                'handlers': ['file_handler']
            },
            'timer': {
                'level': 'INFO',
                'propagate': False,
                'handlers': ['timer_file_handler']
            }
        },
        'handlers': {
            'file_handler': {
                'level': 'INFO',
                'formatter': 'default',
                'class': 'logging.FileHandler',
                'filename': log_file,
                'mode': 'a'
            },
            'timer_file_handler': {
                'level': 'INFO',
                'formatter': 'timer',
                'class': 'logging.FileHandler',
                'filename': log_file,
                'mode': 'a'
            }
        },
        'formatters': {
            'default': {
                'format': '%(asctime)s	%(levelname)s:	File: %(filename)s	Module: %(name)s	Function: `%(funcName)s`	Line: %(lineno)d	%(message)s'
            },
            'timer': {
				'format': '%(asctime)s	%(levelname)s:	%(message)s'
			}
        }
    }

    return LOGGING_CONFIG
