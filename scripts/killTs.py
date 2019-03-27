import subprocess, signal
import os
p = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
out, err = p.communicate()
print "Start Trying to kill all processes of \'runserver\'"
for line in out.splitlines():
    if 'runserver' in line:
        pid = int(line.split()[1])
        print "killing process with id: " + str(pid)
        os.kill(pid, signal.SIGKILL)
        #print line
print "End of process kill runserver"
        
