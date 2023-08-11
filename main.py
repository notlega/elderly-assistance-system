import RPi.GPIO as GPIO
import adxl345
import time
import multiprocessing


LED_MATRIX = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8 ,9],
    ['*', 0, '#']
]
LED_ROW = [6, 20, 19, 13]
LED_COL = [12, 5, 16]


def blink_led(duration = 30):
    start_time = time.time()
    GPIO.setwarnings(False)
    GPIO.setup(24, GPIO.OUT)
    
    while time.time() - start_time > duration:
        GPIO.output(24, 1)
        time.sleep(1)
        GPIO.output(24, 0)
        time.sleep(1)


def buzzer(duration = 30):
    start_time = time.time()
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    
    while time.time() - start_time > duration:
        GPIO.output(18, 1)
        time.sleep(1)
        GPIO.output(18, 0)
        time.sleep(1)


def accelerometer(old_x, old_y, old_z, acc):
    new_x,new_y,new_z = acc.get_3_axis_adjusted()
    if (((new_x - old_x) >= abs(1)) or ((new_y - old_y) >= abs(1)) or (( new_z - old_z) >= abs(1))):
        return 'bing chilling'
    print('bing chilling one')
    time.sleep(0.5)
    accelerometer(new_x, new_y, new_z, acc)


def main():
    # accel_process = multiprocessing.Process(target = accelerometer, args = (x, y, z, acc))
    buzzer_process = multiprocessing.Process(target = buzzer, args = (30, ))
    # accel_process.start()
    buzzer_process.start()
    print(buzzer_process.is_alive())


if __name__ == "__main__":
    ADDRESS=0x53
    GPIO.setmode(GPIO.BCM)

    acc=adxl345.ADXL345(i2c_port=1,address=ADDRESS)
    acc.load_calib_value()
    acc.set_data_rate(data_rate=adxl345.DataRate.R_100)
    acc.set_range(g_range=adxl345.Range.G_16,full_res=True)
    acc.measure_start()
    
    x,y,z=acc.get_3_axis_adjusted()
    
    main()
    
