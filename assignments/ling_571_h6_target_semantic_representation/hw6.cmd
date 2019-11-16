###############################
##LING 571 Homework #5
##Ryan Timbrook (timbrr)
###############################


Executable = /opt/python-3.4.1/bin/python3.4
Universe = vanilla
getenv = true
error = hw6_timbrr_parse.error
Log = hw6_timbrr_parse.log
arguments = hw6_semantics.py hw6_semantic_grammar.fcfg sentences.txt hw6_output.txt
output = hw6_timbrr_parse.out
transfer_executable = false
request_memory = 1024
notify_user = timbrr@u.washington.edu
Queue
