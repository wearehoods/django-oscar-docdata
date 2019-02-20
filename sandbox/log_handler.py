import logging


class SudsLogHandler(logging.StreamHandler):
    """
    Hack log handler for 'suds.transport', that
    just "reformat" newlines in binary representations
    """
    def emit(self, record):
        try:
            msg = self.format(record)

            msg = msg.replace("\\n", "\n") # Hack ;)

            stream = self.stream
            stream.write(self.terminator)
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)
