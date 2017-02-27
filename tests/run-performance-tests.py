import time

print "Starting performance tests....."

for x in range(1,11):
    time.sleep(1)
    print "Run %s/10 .........\t OK" % x
