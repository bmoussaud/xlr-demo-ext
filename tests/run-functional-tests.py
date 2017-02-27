import time
import sys

print "Starting functional tests....."

for x in range(1,11):
    time.sleep(1)
    if x == 4:
        print "Run %s/10 .........\t KO" % x
        sys.exit(1)
    else:
        print "Run %s/10 .........\t OK" % x

