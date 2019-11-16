###############################
##LING 571 Homework #9
##Ryan Timbrook (timbrr)
###############################


Executable = /opt/python-3.4.1/bin/python3.4
Universe = vanilla
getenv = true
error = hw9_timbrr_parse.error
Log = hw9_timbrr_parse.log
arguments = hw9_coref.py grammar.cfg coref_sentences.txt hw9_output.txt
output = hw9_timbrr_parse.out
transfer_executable = false
request_memory = 2*1024
notify_user = timbrr@u.washington.edu
Queue
