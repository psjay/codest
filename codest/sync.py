#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import subprocess
import logging
from threading import RLock, Thread


class SyncRunner(Thread):

    def __init__(self, sync, **kwargs):
        super(SyncRunner, self).__init__(**kwargs)
        self._sync = sync
        self._stopped = False

    def run(self):
        while not self._stopped:
            time.sleep(self._sync.interval)
            self._sync.sync()

    def stop(self):
        self._stopped = True


class Sync(object):

    def __init__(self, path, remote_path, interval=3):
        self._path = path
        self._remote_path = remote_path
        self.interval = interval

        self._abspath = os.path.abspath(self._path)
        self._paths_to_sync = set([])
        self._lock = RLock()
        self._runner = SyncRunner(self)

    def sync_root(self):
        params = ['rsync', '-aqzR', '--delete', '--exclude=.git', '--filter=:- /.gitignore']
        params.append(self._cal_path_with_implied_dirs(self._path))
        params.append(self._remote_path)
        subprocess.Popen(params).wait()

    def sync(self):
        paths_to_sync = None
        with self._lock:
            paths_to_sync = self._paths_to_sync
            self._paths_to_sync = set([])
        if paths_to_sync:
            logging.info('Syncing:%s%s', os.linesep, os.linesep.join(
                [os.path.relpath(p) for p in paths_to_sync]
            ))
            self._rsync_paths(paths_to_sync)

    def _rsync_paths(self, paths):
        params = ['rsync', '-dqR', '--delete', '--delete-missing-args']
        params.extend([self._cal_path_with_implied_dirs(p) for p in paths])
        params.append(self._remote_path)
        subprocess.Popen(params).wait()

    def _cal_path_with_implied_dirs(self, file_path):
        relpath = os.path.relpath(file_path, self._abspath)
        return os.path.join(self._path, '.', relpath)

    def start(self):
        self._runner.start()

    def stop(self):
        self._runner.stop()
        self._runner.join()

    def add_path(self, path):
        with self._lock:
            self._paths_to_sync.add(os.path.abspath(path))

    def remove_path(self, path):
        with self._lock:
            abs_path = os.path.abspath(path)
            if abs_path in self._paths_to_sync:
                self._paths_to_sync.remove(abs_path)
