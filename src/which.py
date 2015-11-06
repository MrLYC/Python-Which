#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
import os
import platform

PLATFORM_NAME = platform.system()


class WhichCommand(object):
    def __init__(self, name):
        self.name = name
        
    @property
    def path_list(self):
        path = os.environ.get("PATH", "")
        return path.split(os.pathsep)
    
    def is_executable(self, path):
        if not os.path.isfile(path) and not os.path.islink(path):
            return False
        if PLATFORM_NAME == "Windows":
            return True
        return os.access(path, os.X_OK)
        
    def find(self):
        for p in self.path_list:
            if not os.path.isdir(p):
                continue
            for f in os.listdir(p):
                path = os.path.join(p, f)
                if f == self.name and self.is_executable(path):
                    yield path


if __name__ == "__main__":
    parser = ArgumentParser("which - locate a command")
    parser.add_argument("filename")
    parser.add_argument(
        "-a", dest="all", action="store_true",
        help="print all matching pathnames of each argument",
    )
    args = parser.parse_args()
    which_cmd = WhichCommand(args.filename)
    existed = False
    for p in which_cmd.find():
        print p
        existed = True
        if not args.all:
            break
    if not existed:
        parser.exit(1)
    parser.exit(0)
