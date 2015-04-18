#! /bin/bash
# Richard Kirchofer

dd if=/dev/urandom of=foo bs=50K count=1
# 1+0 records in
# 1+0 records out
# 1048576 bytes (1.0 MB) copied, 0.303966 s, 3.4 MB/s

time python idea-ctr-file.py foo
# python idea-ctr-file.py foo  28.02s user 0.03s system 99% cpu 28.099 total

time python idea-ctr-file.py foo.idea foo.key
# python idea-ctr-file.py foo.idea foo.key  25.39s user 0.06s system 99% cpu 25.514 total

diff -s foo foo.idea
# Binary files foo and foo.idea differ

diff -s foo foo.idea.idea
# Files foo and foo.idea.idea are identical

# In order to build the pdf from the .tex file, run make with the provided make file.

# In order to benchmark the program, run ./kernprof -lv idea-ctr-file.py foo bar.
 
# Examples to run the program are provided in the report.
 
# LaTeX makefile credit:
# Copyright 2004 Chris Monson (shiblon@gmail.com)
# Latest version available at http://www.bouncingchairs.net/oss
 
# kernprof python line profiler credit:
# Robert Kern
# robert.kern@gmail.com
