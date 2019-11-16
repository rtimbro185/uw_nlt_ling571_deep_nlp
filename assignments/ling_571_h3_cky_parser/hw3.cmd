###############################
##
##LING 571 Homework #3
##Ryan Timbrook (timbrr)
###############################

Executable = /opt/python-3.4.1/bin/python3.4
Universe = vanilla
getenv = true
error = ./logs/hw3_timbrr_parse.error
Log = ./logs/hw3_timbrr_parse.log
arguments = hw3_parser.py grammar_cnf.cfg sentences.txt hw3_output.txt
output = ./logs/hw3_timbrr_parse.out
transfer_executable = false
request_memory = 1024
notify_user = timbrr@u.washington.edu
Queue
