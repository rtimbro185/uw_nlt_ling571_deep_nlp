###############################
##
##LING 571 Homework #1
##Ryan Timbrook (timbrr)
###############################

Executable = /opt/python-3.4.1/bin/python3.4
Universe = vanilla
getenv = true
error = hw1_timbrr_parse.error
Log = hw1_timbrr_parse.log
arguments = hw1_parse.py hw1_grammar.cfg sentences.txt hw1_output.txt
output = hw1_timbrr_parse.out
transfer_executable = false
request_memory = 1024
notify_user = timbrr@u.washington.edu
Queue
