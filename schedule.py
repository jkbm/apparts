from appartments import get_appartments
import sched, time

#Execute get_appartments function every n minutes
wait = 300 # time to wait before getting data again(in seconds)
while True:
    get_appartments(web=False)
    time.sleep(wait)