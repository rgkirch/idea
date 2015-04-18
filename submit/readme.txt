Richard Kirchofer
idea-ctr-file.py
https://github.com/rgkirch/idea
$ git clone git@github.com:rgkirch/idea.git

$ cd run

if not already

$ chmod +x run.sh

then

$ ./run.sh

In order to build the pdf from the .tex file, run make with the provided make file.

In order to benchmark the program, run ./kernprof -lv idea-ctr-file.py foo bar.
 
Examples to run the program are provided in the report.
 
LaTeX makefile credit:
Copyright 2004 Chris Monson (shiblon@gmail.com)
Latest version available at http://www.bouncingchairs.net/oss
 
kernprof python line profiler credit:
Robert Kern
robert.kern@gmail.com
