#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess


def git2rsync(lines, path):
    converted = []
    for line in lines:
        line = line.rstrip('\n')
        if not line.strip() or line.startswith('#'):
            continue

        if line[0] == '\\':
            line = line[1:]
        if line[0] != '/' and '/' in line[1:-1]:
            line = '/' + line
        if line[0] == '/':
            path = path.rstrip('/')
            line = '/' + os.path.basename(path) + line

        converted.append(line)

    return converted


def is_git_ignored(path):
    r = subprocess.call(['git', 'check-ignore', '-q', path])
    return r == 0
