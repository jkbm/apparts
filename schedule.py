from appartments import get_appartments
import sched, time

#Execute get_appartments function every n minutes
wait = 300 # time to wait before getting data again(in seconds)
executes = 0
while True:
    get_appartments(web=False)
    executes += 1
    print("\nScript executed %s times." % executes)
    time.sleep(wait)