#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging
import subprocess
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from codest.repository import Repository, GitRepository
from codest.sync import Sync


logger = logging.getLogger(__name__)


class CodestEventHandler(FileSystemEventHandler):

    def __init__(self, sync, repos):
        super(CodestEventHandler, self).__init__()

        self._sync = sync
        self._repos = repos

        self._sync.start()

    def on_any_event(self, event):
        repo = match_repo(event.src_path, self._repos)
        file_path = repo.filter_path(event.src_path)
        if file_path:
            self._sync.add_path(file_path)

    def stop_sync(self):
        self._sync.stop()


def load_repos(path):
    p1 = subprocess.Popen(('find %s -name .git -type d -prune' % path).split(' '), stdout=subprocess.PIPE)
    p2 = subprocess.Popen('xargs -n 1 dirname'.split(' '), stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    git_paths = p2.communicate()[0].split(os.linesep)[:-1]
    git_paths.sort(key=lambda x: (x, -1 * len(x.split(os.path.sep))))
    repos = [GitRepository(p) for p in git_paths]
    if path not in git_paths:
        repos.append(Repository(path))
    return repos


def match_repo(path, candidates):
    for repo in candidates:
        if path.startswith(os.path.abspath(repo.path)):
            return repo
    return None


def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--sync-only', dest='sync_only',
                           action='store_true', default=False, help='Do a sync, then exit.')
    argparser.add_argument('-i', '--interval', dest='interval', type=int, default=3,
                           help='Sync interval in seconds, defaults to 3.')
    argparser.add_argument('path', nargs='?', default=os.getcwd(), help='Local path to be synced')
    argparser.add_argument('remote_path', type=str, help='Remote path.')
    args = argparser.parse_args()
    return args


def config_logger():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


def main():
    config_logger()
    args = parse_args()

    repos = load_repos(args.path)
    sync = Sync(args.path, args.remote_path,
                interval=args.interval)

    logging.info('Syncing recursively: %s', args.path)
    sync.sync_root()

    if args.sync_only:
        return

    # set up monitor
    event_handler = CodestEventHandler(sync, repos)
    observer = Observer()
    observer.schedule(event_handler, os.path.abspath(args.path), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info('codest will exit after the current sync.')
        event_handler.stop_sync()
    observer.join()


if __name__ == '__main__':
    main()
