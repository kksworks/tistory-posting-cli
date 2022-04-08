#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os
import time, datetime

import inspect
import logging
import logging.handlers

class logTool() :
    log_level_str = {'debug': logging.DEBUG, 'info': logging.INFO, 'error' : logging.ERROR }

    def __init__(self, loger_name, log_level = 'debug', logfile_path = None, logfile_size_kb = 0 ):
        self.loger_name = loger_name
        self.logger = logging.getLogger(self.loger_name)
        # default initialize for logging class..
        self.logger.setLevel(self.log_level_str[log_level])

        # log file setting
        if logfile_size_kb > 0 and logfile_path is not None :
            self.set_log_files(logfile_size_kb, logfile_path)

        self._set_loger_init()

    def set_log_level(self, log_level) :
        self.logger.setLevel(self.log_level_str[log_level])

    def _set_loger_init(self) :
        class InfoFilter(logging.Filter):
            def filter(self, rec):
                return rec.levelno in (logging.DEBUG, logging.INFO, logging.ERROR)


        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.addFilter(InfoFilter())
        self.logger.addHandler(stdout_handler)

        #stderr_handler = logging.StreamHandler(sys.stderr)
        #stderr_handler.setLevel(logging.ERROR)
        #stderr_handler.addFilter(InfoFilter())
        #self.logger.addHandler(stderr_handler)

    def set_log_files(self, log_size_kb, log_path) :
        fileMaxByte = 1024 * 1024 * log_size_kb
        self.fileHandler = logging.handlers.RotatingFileHandler(log_path, maxBytes=fileMaxByte, backupCount=10)
        self.logger.addHandler(self.fileHandler)


    def _debug_msg_print(self, log_level, caller_name_str, msg):
        timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print_msg = '[{timestamp_str} | {log_level}\t] - {caller_name_str}() : {msg}'.format(timestamp_str=timestamp_str, log_level=log_level, caller_name_str=caller_name_str, msg=str(msg) )

        if log_level == 'debug' :
            self.logger.debug (print_msg)

        if log_level == 'info' :
            self.logger.info (print_msg)

        if log_level == 'err' :
            self.logger.error (print_msg)
            # print(print_msg,file=sys.stderr)

    def err(self, msg) :
        caller_name_str = str(inspect.stack()[1][3])
        self._debug_msg_print('err', caller_name_str, msg)

    def info(self, msg) :
        caller_name_str = str(inspect.stack()[1][3])
        self._debug_msg_print('info', caller_name_str, msg)

    def dbg(self, msg) :
        caller_name_str = str(inspect.stack()[1][3])
        self._debug_msg_print('debug', caller_name_str, msg)


if __name__ == '__main__':
    def hello() :
        log_ctx = logTool('hello world', log_level='info', logfile_path = 'logtest.log', logfile_size = 100)
        log_ctx.dbg('hello-dbug')
        log_ctx.info('hello-info')
    
    hello()