###############################
##
##LING 571 Homework #2
##Ryan Timbrook (timbrr)
###############################

Executable = /opt/python-3.4.1/bin/python3.4
Universe = vanilla
getenv = true
error = ./logs/hw2_timbrr_parse.error
Log = ./logs/hw2_timbrr_parse.log
arguments = hw2_tocnf.py atis.cfg hw2_grammar_cnf.cfg
output = ./logs/hw2_timbrr_parse.out
transfer_executable = false
request_memory = 1024
notify_user = timbrr@u.washington.edu
Queue
