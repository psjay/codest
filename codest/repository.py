#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen


class Repository(object):

    def __init__(self, path):
        self.path = path

    def filter_path(self, path):
        return path


class GitRepository(Repository):

    def __init__(self, path):
        super(GitRepository, self).__init__(path)
        self._ignored_files = set()

    def is_ignored(self, relpath):
        if relpath.endswith('.git') or '.git/' in relpath:
            return True
        if relpath.endswith('.gitignore'):
            self._ignored_files = set([])
        if relpath in self._ignored_files:
            return True
        if self._check_ignore(relpath):
            self._ignored_files.add(relpath)
            return True
        return False

    def _check_ignore(self, relpath):
        cwd = os.getcwd()
        try:
            os.chdir(self.path)
            params = ['git', 'check-ignore', '-q', relpath]
            ret = Popen(params).wait()
            return ret == 0
        finally:
            os.chdir(cwd)

    def filter_path(self, path):
        relpath = os.path.relpath(path, os.path.abspath(self.path))
        if not self.is_ignored(relpath):
            return path
