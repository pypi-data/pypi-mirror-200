import inspect
import logging
import time
import os


class Logger():
    def __init__(self, log_name=None, log_path=None, log_level=None):

        if log_name:
            self.log_name = log_name
        else:
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            filename = module.__file__
            self.log_name = os.path.basename(filename)

        dict_logging = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARN": logging.WARNING,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        self.time = None
        self.time_start = None
        self.time_end = None

        if log_level:
            log_level = str(log_level).upper()
            try:
                self.log_level = dict_logging[log_level]
            except Exception as e:
                self.log_level = dict_logging["DEBUG"]
        else:
            self.log_level = dict_logging["DEBUG"]

        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(self.log_level)

        if log_path:
            self.log_file = os.path.join(log_path, self.log_name + ".log")
        else:
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            filename = module.__file__
            current_path = os.path.dirname(os.path.abspath(filename))
            self.log_file = os.path.join(current_path, self.log_name + ".log")

        # formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s', "%Y-%m-%d %H:%M:%S")
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")

        file_handler = logging.FileHandler(self.log_file, encoding="UTF-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def format_seconds_to_hhmmss(self, seconds):
        hours = seconds // (60 * 60)
        seconds %= (60 * 60)
        minutes = seconds // 60
        seconds %= 60
        return "%02i:%02i:%02i" % (hours, minutes, seconds)

    def timer_start(self):
        self.log(F"[LOGGER] Timer Start")
        self.time = time.time()

    def timer_stop(self):
        t = time.time()
        i = t - self.time
        txt = "{:.3f}".format(i)
        self.log(F"[LOGGER] Finished in {txt}s")
        return txt

    def log(self, message, level=None):
        if not level:
            self.logger.info(message)
        elif level.upper() == "INFO":
            self.logger.info(message)
        elif level.upper() == "WARN":
            self.logger.warn(message)
        elif level.upper() == "WARNING":
            self.logger.warning(message)
        elif level.upper() == "DEBUG":
            self.logger.debug(message)
        elif level.upper() == "ERROR":
            self.logger.error(message)
        else:
            self.logger.info(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def touch(self, check_file):
        if os.path.exists(check_file):
            pass
        else:
            open(check_file, 'a').close()
            self.info(F"[LOGGER] Creating File : {os.path.basename(check_file)}")


if __name__ == "__main__":
    log = Logger()
    log.log("DEFAULT !!")
    log.debug("DEBUG !!")
    log.info("INFO !!")
    log.warning("WARNING !!")
    log.error("ERROR !!")
    log.critical("CRITICAL !!")
