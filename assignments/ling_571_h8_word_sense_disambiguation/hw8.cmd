###############################
##LING 571 Homework #8
##Ryan Timbrook (timbrr)
###############################


Executable = /opt/python-3.4.1/bin/python3.4
Universe = vanilla
getenv = true
error = hw8_timbrr_parse.error
Log = hw8_timbrr_parse.log
arguments = hw8_resnik_wsd.py nltk wsd_contexts.txt hw8_output.txt
output = hw8_timbrr_parse.out
transfer_executable = false
request_memory = 2*1024
notify_user = timbrr@u.washington.edu
Queue
