#!/usr/bin/python

import sys, os, os.path, string, glob, math
import time, datetime
import argparse


def job_id(arg):
    emsg = "Invalid job-id value: '%s\'" % (arg)
    vl = arg.strip().split('.')
    if len(vl) != 2: raise argparse.ArgumentTypeError(emsg)
    try:
       clust = int(vl[0])
       proc = int(vl[1])
    except:
       raise argparse.ArgumentTypeError(emsg)
    return (clust, proc)


def time_spec(arg):
    t0 = int(time.time())
    date0 = time.strftime("%Y/%m/%d")

    emsg = "Unrecognized time spec value: '%s'" % (arg)

    vl = arg.strip().split()

    # interpret integer arg as 'seconds since Big Bang'
    try:
        if len(vl) != 1: raise Exception()
        t = int(vl[0])
    except: pass
    else:
        return t


    # interpret times like '10 min ago'  ('ago' may be left off)
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
        return t


    # interpret some 'sleep-style' times, like '10s', '5m', etc.  These are implicitly 'ago'
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
        return t


    # interpret some specific date/time formats
    for fmt in ["%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M", "%Y/%m/%d"]:
        try:
            t = int(time.mktime(time.strptime(" ".join(vl), fmt)))
        except: pass
        else:
            return t


    # interpret "%H:%M:%S", etc  (y/m/d is taken as current date)
    for fmt in ["%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M"]:
        tstr = date0 + " " + " ".join(vl)
        try:
            t = int(time.mktime(time.strptime(tstr, fmt)))
        except: pass
        else:
            return t

    # if none of the above apply, we failed to parse and it's an error
    raise argparse.ArgumentTypeError(emsg)



class time_arg_parser(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list): vl = " ".join(values)
        else: vl = values

        try:
            t = time_spec(vl)
        except: pass
        else:
            setattr(namespace, self.dest, t)
            return

        # we failed to parse and it's an error
        sys.stderr.write("bad time format\n\n")
        parser.print_help()
        sys.exit(1)
        
