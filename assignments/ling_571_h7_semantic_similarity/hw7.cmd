###############################
##LING 571 Homework #5
##Ryan Timbrook (timbrr)
###############################


Executable = /opt/python-3.4.1/bin/python3.4
Universe = vanilla
getenv = true
error = hw7_timbrr_parse.error
Log = hw7_timbrr_parse.log
arguments = hw7_dist_similarity.py 2 FREQ mc_similarity.txt hw7_sim_2_FREQ_output.txt
output = hw7_timbrr_parse.out
transfer_executable = false
request_memory = 1024
notify_user = timbrr@u.washington.edu
Queue
