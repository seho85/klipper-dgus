import time, sys

sleep_time = sys.argv[1] if len(sys.argv) > 1 else 15

try:
        sleep_time = int(sleep_time)
except ValueError:
        sleep_time = 15

time.sleep(sleep_time)
