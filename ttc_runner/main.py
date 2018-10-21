from testopencv import DetectAndRun
import time


dt_check = 3  # Period to check clova. 
ttc = DetectAndRun()

while True:
    ttc.run()
    time.sleep(dt_check)
