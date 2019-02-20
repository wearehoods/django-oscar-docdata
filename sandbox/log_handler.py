"""
    Hacked log handler for 'suds.transport', that
    just "reformat" newlines in binary representations

    Usage, e.g.:

        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                },
                'suds_handler': {
                    'class': 'sandbox.log_handler.SudsLogHandler',
                }
            },
            'loggers': {
                # ...
                'suds.transport': {
                    'handlers': ['suds_handler'],
                    'level': 'DEBUG' if DEBUG is True else 'INFO',
                    'propagate': True,
                },
                '# ...
            },
        }
"""

import logging

from django.conf import settings

# Hide the settings values from theses settings:
HIDE_SETTING_NAMES = ("DOCDATA_MERCHANT_NAME", "DOCDATA_MERCHANT_PASSWORD")


class SudsLogHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            # Note: We get the "suds.transport" log output as strings.
            # e.g.: MESSAGE is only a string representation of bytes.

            # The Hack: reformat newlines:
            msg = msg.replace("\\n", "\n")

            # Replace sensitive setting values like passwords from log output:
            for settings_name in HIDE_SETTING_NAMES:
                settings_value = getattr(settings, settings_name, None)
                if settings_value:
                    if "\\" in settings_value:
                        # e.g.: password contains a "\"-character
                        # a normal replace will not match this
                        # we have to replace the escaped version here
                        settings_value = settings_value.replace("\\", "\\\\")

                    msg = msg.replace(settings_value, "***")

            # Do the output with some newlines:
            stream = self.stream
            stream.write(self.terminator)
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)
