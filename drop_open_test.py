from nine_axis import *
from parachute import *

drop_counter = 0
stop_counter = 0

#drop_counterは試験をして調整
while drop_counter < 1:
    az = get_az()
    print("not detect drop")
    if az > 1:
        drop_counter = drop_counter + 1
    time.sleep(0.25)
    

while stop_counter < 12:
    az = get_az()
    print("not detect stop")
    if abs(az) < 0.01:
        stop_counter = stop_counter + 1
    time.sleep(0.25)

parachute_sep()