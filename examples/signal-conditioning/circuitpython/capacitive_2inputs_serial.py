import time
import board
import touchio

touch_pad1 = board.IO4
touch_pad2 = board.IO6

touch1 = touchio.TouchIn(touch_pad1)
touch2 = touchio.TouchIn(touch_pad2)

TX_RATE = 0.02
LAST_LOOP_TIME = -1


"""Maps a value x from range [input_min, input_max] to [output_min, output_max]."""
def transform_range(x, input_min, input_max, output_min, output_max):
    return output_min + ( (x - input_min) * (output_max - output_min) ) / (input_max - input_min)


while True:
    
    now = time.monotonic()
    if now >= LAST_LOOP_TIME + TX_RATE:
        #print(touch1.raw_value,touch2.raw_value)
        print(transform_range(touch1.raw_value, 11200, 65535, 0, 1),transform_range(touch2.raw_value, 12600, 65535, 0, 1))
        LAST_LOOP_TIME = time.monotonic()
