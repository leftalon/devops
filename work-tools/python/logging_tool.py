#!/usr/bin/env python
# encoding:utf-8

import logging
import os
import logging.handlers

class Logging(object):
        def __init__(self,log_path,log_name):
                log_dir = os.path.dirname(log_path)
                if not os.path.exists(log_dir):
                        os.mkdir(log_dir)
                self.logger_name = logging.getLogger(log_name)
                self.logger_name.setLevel(logging.DEBUG)

                self.file_handler = logging.handlers.TimedRotatingFileHandler(log_path)
                self.file_handler.setLevel(logging.DEBUG)
                formatter = logging.Formatter("%(asctime)s--%(name)s--%(levelname)s--%(message)s")
                self.file_handler.setFormatter(formatter)
                self.logger_name.addHandler(self.file_handler)


log_path="/data1/test/test.log"
log_name="test"
c=Logging(log_path,log_name)
c.logger_name.info("is info")
c.logger_name.debug("id debug")

