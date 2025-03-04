import time
import board
import touchio
import math

touch_pad1 = board.IO4
touch_pad2 = board.IO6

touch1 = touchio.TouchIn(touch_pad1)
touch2 = touchio.TouchIn(touch_pad2)

TX_RATE = 0.02
LAST_LOOP_TIME = -1

alpha = 0.9
activate_filter = True  

touch1_filtered = 0.0
touch2_filtered = 0.0

growth_factor = 3 # Try values between 2-10 for different effects
log_factor = 20   # Try values between 5-20 for different effects

"""Maps a value x from range [input_min, input_max] to [output_min, output_max]."""
def transform_range(x, input_min, input_max, output_min, output_max):
    return output_min + ( (x - input_min) * (output_max - output_min) ) / (input_max - input_min)

def exponential_response(raw_value):
    """Apply exponential growth to touch input."""
    return (math.exp(raw_value * growth_factor) - 1) / (math.exp(growth_factor) - 1)

def logarithmic_response(raw_value):
    """Apply a logarithmic transformation to reduce response for strong touches."""
    return math.log(1 + raw_value * log_factor) / math.log(1 + log_factor)

while True:
    
    now = time.monotonic()
    if now >= LAST_LOOP_TIME + TX_RATE:
        
        #perform normalization to range (0,1)
        touch1_normalized = transform_range(touch1.raw_value, 11650, 65535, 0, 1)
        touch2_normalized = transform_range(touch2.raw_value, 12600, 65535, 0, 1)
        
        #perform exponential smoothing
        if activate_filter is False:
            touch1_filtered  = touch1_normalized
            touch2_filtered  = touch2_normalized
            
        else:
            touch1_filtered = alpha * touch1_normalized + (1 - alpha) * touch1_filtered
            touch2_filtered = alpha * touch2_normalized + (1 - alpha) * touch2_filtered

        #perform precision reduction and round last decimal
        touch1_filtered = round(touch1_filtered, 3)  #last argument is the number of decimals
        touch2_filtered = round(touch2_filtered, 3)
        
        #apply exponential response
        touch1_exp = exponential_response(touch1_filtered)
        touch2_exp = exponential_response(touch2_filtered)
        
        touch1_exp = round(touch1_exp, 3)  #last argument is the number of decimals
        touch2_exp = round(touch2_exp, 3)
        
        #print(touch1_filtered ,touch1_exp) #to check difference
        print(touch1_exp ,touch2_exp) #transmit both filtered values
        
        LAST_LOOP_TIME = time.monotonic()
