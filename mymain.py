#!/usr/bin/env python3

import os
import sys
import mykook as kook

parser = kook.KOOK()
for arg in range(1, len(sys.argv)):
    name, ext = os.path.splitext(sys.argv[arg])
    print("File name:", name, "& file extention:", ext)
    if ext == ".kc" or ext == ".kh":
        try:
            print("Implementation of files to get to c/h", sys.argv[arg])
            res = kook.get_tree(sys.argv[arg])
            print("Turning kook code to C from file:", sys.argv[arg])
            print("RES Writen:")
            print(res)
        except Exception as e:
            print("Kook to_c content recuperation FAILED")
            print("Diagnostic args are:", e.args)
            print("Diagnostic traceback is:", e.with_traceback(None))
    elif ext == ".c" or ext == ".h":
        res = kook.get_tree(sys.argv[arg])
        print("Normal", ext, " C/H file treated:", sys.argv[arg])
        print("with resulting code:")
        print(res)
    else:
        print("could not get kook:", sys.argv[arg], "file.")

