import machine
import utime

# Initialize UART1
uart1 = machine.UART(1, tx=machine.Pin(4), rx=machine.Pin(5), baudrate=9600)

# Initialize stepper motor pins
step_pin = machine.Pin(2, machine.Pin.OUT)
dir_pin = machine.Pin(3, machine.Pin.OUT)

# Flags
emergency_stop_flag = False
jogging_mode_flag = False

# Counter
step_counter = 0

# Settings
steps_todo = 0
delay = 0.001
initial_delay = 0.002

# Function to reset the counter and settings
def reset_counter():
    global step_counter, steps_todo
    step_counter = 0
    steps_todo = 0

# Main function
def main():
    global emergency_stop_flag, jogging_mode_flag, step_counter, steps_todo

    while True:
        # Read UART if available
        if uart1.any():
            received_char = uart1.read(1).decode('ascii')
            print("Received:", received_char)
            
            if received_char == 'A':
                reset_counter()
                steps_todo = 3000
                print("Running 3000 steps")
                
            elif received_char == 'B':
                reset_counter()
                steps_todo = 6000
                print("Running 6000 steps")
                
            elif received_char == 'C':
                print("Emergency Stop")
                emergency_stop_flag = True
                
            elif received_char == 'D':
                print("Entering Jogging Mode")
                jogging_mode_flag = True
                
            elif received_char == 'E':
                print("Exiting Jogging Mode")
                jogging_mode_flag = False
                
        # Run stepper
        if steps_todo > 0 and not emergency_stop_flag:
            step_pin.value(1)
            utime.sleep_us(300)
            step_pin.value(0)
            utime.sleep_us(300)
            if step_counter < 50:
                utime.sleep(initial_delay)
            else:
                utime.sleep(delay)
            step_counter += 1
            steps_todo -= 1
        
        # Check emergency stop
        if emergency_stop_flag:
            reset_counter()
            emergency_stop_flag = False
        
        # Check jogging mode
        if jogging_mode_flag and not emergency_stop_flag:
            step_pin.value(1)
            utime.sleep_us(300)
            step_pin.value(0)
            utime.sleep_us(300)
            utime.sleep(delay)

if __name__ == "__main__":
    main()

