# import RPi.GPIO as GPIO
import time
import multiprocessing
import classes.dht11 as dht11


## comf temp 23 - 26
## moisture 30% - 50%


def main():
    fall_bool = False
    button_bool = False
    signal_bool = False

    blink_process = multiprocessing.Process(target=blink_led, args=(30,))
    instance = dht11.DHT11(pin = 21)

    while True:
        time_strings = time.strftime("%Y,%m,%d,%H,%M,%S")
        time_list = time_strings.split(",")
        time_num = [ int(x) for x in time_list ]
        
        dht_result = instance.read()

        if time_num[3] == 12:
            ## check daily shit at noon
            pass

        if fall_bool:
            blink_process.start()

        if signal_bool:
            blink_process.kill()

        time.sleep(0.5)
            

def blink_led(duration = 30):
    start_time = time.time()
    GPIO.setwarnings(False)
    GPIO.setup(24, GPIO.OUT)

    while time.time() - start_time > duration:
        GPIO.output(24, 1)
        time.sleep()
        GPIO.output(24, 0)
        time.sleep()


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    main()

