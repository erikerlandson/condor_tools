#!/usr/bin/python

import sys, os, os.path, string, glob, math
import time, datetime
import argparse


class time_arg_parser(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        t0 = int(time.time())

        vl = []
        if isinstance(values, list): vl = values
        else: vl = values.strip().split()

        try:
            if len(vl) != 1: raise Exception()
            t = int(vl[0])
        except: pass
        else:
            setattr(namespace, self.dest, t)
            return

        try:
            if not (len(vl) in [2,3]): raise Exception()
            if (len(vl) == 3) and (vl[2] != 'ago'): raise Exception()
            smx = 1
            if vl[1] in ['seconds', 'second', 'secs', 'sec', 's']: smx = 1
            elif vl[1] in ['minutes', 'minute', 'min', 'm']: smx = 60
            elif vl[1] in ['hours', 'hour', 'h']: smx = 3600
            elif vl[1] in ['days', 'day', 'd']: smx = 24 * 3600
            elif vl[1] in ['weeks', 'week', 'w']: smx = 7 * 24 * 3600
            else: raise Exception()
            t = t0 - (smx * int(vl[0]))
        except: pass
        else:
            setattr(namespace, self.dest, t)
            return

        try:
            if len(vl) != 1: raise Exception()
            tt = vl[0][:-1]
            ss = vl[0][-1:]
            smx = 1
            if ss == 's': smx = 1
            elif ss == 'm': smx = 60
            elif ss == 'h': smx = 3600
            elif ss == 'd': smx = 24*3600
            elif ss == 'w': smx = 7*24*3600
            else: raise Exception()
            t = t0 - (smx * int(tt))            
        except: pass
        else:
            setattr(namespace, self.dest, t)
            return

        # if none of the above apply, we failed to parse and it's an error
        sys.stderr.write("bad time format\n\n")
        parser.print_help()
        sys.exit(1)
        
