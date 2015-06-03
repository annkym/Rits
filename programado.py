import sched, time
s = sched.scheduler(time.time, time.sleep)
def print_time(): print "From print_time()", time.time()
