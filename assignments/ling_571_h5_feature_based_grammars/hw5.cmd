###############################
##LING 571 Homework #5
##Ryan Timbrook (timbrr)
###############################


Executable = /opt/python-3.4.1/bin/python3.4
Universe = vanilla
getenv = true
error = hw5_timbrr_parse.error
Log = hw5_timbrr_parse.log
arguments = hw5_parser.py hw5_feature_grammar.fcfg sentences.txt hw5_output.txt
output = hw5_timbrr_parse.out
transfer_executable = false
request_memory = 1024
notify_user = timbrr@u.washington.edu
Queue
