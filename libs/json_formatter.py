# encoding=utf-8
import logging
import time
import sys
import json

class JSONFormatter(logging.Formatter):
    '''
        把日志格式化成json格式，以便大数据收集
    '''
    converter = time.localtime

    def __init__(self, service=None):
        '''

        :param service: 业务标识
        '''
        self.service = service

    def format(self, record):
        s = record.getMessage()
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            try:
                s = s + record.exc_text
            except UnicodeError:
                # Sometimes filenames have non-ASCII chars, which can lead
                # to errors when s is Unicode and record.exc_text is str
                # See issue 8924.
                # We also use replace for when there are multiple
                # encodings, e.g. UTF-8 for the filesystem and latin-1
                # for a script. See issue 13232.
                s = s + record.exc_text.decode(sys.getfilesystemencoding(),
                                               'replace')

        task_id = record.__dict__.get("task_id", "")

        dd = {
            "service": self.service,
            "name": record.name,
            "level": record.levelname,
            "pathname": record.pathname,
            "lineno": record.lineno,
            "msg": s,
            "log_date": self.formatTime(record),
            "task_id": task_id
        }
        return json.dumps(dd)

    def formatTime(self, record, datefmt="%Y-%m-%dT%H:%M:%S+0800"):
        '''

        :param record:
        :param datefmt:
        :return:
        '''
        ct = self.converter(record.created)
        return time.strftime(datefmt, ct)
