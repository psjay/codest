#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import time
import threading

from livecode import ignore_rule


class Repository(object):

    def __init__(self, path, remote_path):
        self._path = path
        self._remote_path = remote_path
        self._last_sync = 0
        self._ignore_rules = '\n'.join(self._convert_ignore_file(self._path))

    @staticmethod
    def validate_path(path):
        if os.path.exists(os.path.join(path, '.git')):
            return True
        return False

    def _convert_ignore_file(self, repo_path):
        if not os.path.exists(os.path.join(repo_path, '.gitignore')):
            return ''

        with open(os.path.join(repo_path, '.gitignore'), 'r') as ignore_file:
            lines = ignore_file.readlines()
            return ignore_rule.git2rsync(lines, self._path)

    def _do_sync(self):
        print 'Start to sync.'
        rsync = subprocess.Popen(['rsync', '-av', '--delete',
                                  '--exclude=.git/', '--exclude-from=-',
                                  self._path, self._remote_path],
                                 stdin=subprocess.PIPE)
        rsync.communicate(input=self._ignore_rules)

    def sync(self):
        now = time.time()
        if self._last_sync == 0:
            self._last_sync = now
            self._do_sync()
        else:
            if now < self._last_sync:
                return
            else:
                self._last_sync = now + 1
                t = threading.Timer(1, self._do_sync)
                t.start()
