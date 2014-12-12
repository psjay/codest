#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import logging
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from livecode import ignore_rule
from livecode.repository import Repository


logger = logging.getLogger(__name__)


class LiveCodeEventHandler(FileSystemEventHandler):

    def __init__(self, repo):
        self._repo = repo

    def on_any_event(self, event):
        if event.src_path.endswith('.git') or event.src_path.endswith('.git/'):
            return
        if '.git/' in event.src_path:
            return
        if ignore_rule.is_git_ignored(event.src_path):
            return
        print '[%s %s] %s.' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), event.event_type.upper(), event.src_path)
        self._repo.sync()


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--sync-only', dest='sync_only',
                           action='store_true', default=False, help='Do a sync, then exit.')
    argparser.add_argument('path', nargs='?', default=os.getcwd(), help='Local Git repository path.')
    argparser.add_argument('remote_path', type=str, help='Remote path.')
    args = argparser.parse_args()
    path = os.path.abspath(args.path).rstrip('/')
    remote_path = args.remote_path.rstrip('/')

    if not Repository.validate_path(path):
        print 'ERROR: Not a git repository.'
        exit(1)

    os.chdir(path)
    repo = Repository(path, remote_path)

    print 'Sync on startup.'
    repo.sync()

    if args.sync_only:
        return

    # set up monitor
    event_handler = LiveCodeEventHandler(repo)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
