import RPi.GPIO as GPIO
import I2C_LCD_driver
import dht11
import adxl345
import time
import telegram
import multiprocessing
import asyncio

LED_MATRIX = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8 ,9],
    ['*', 0, '#']
]
LED_ROW = [6, 20, 19, 13]
LED_COL = [12, 5, 16]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ADDRESS = 0x53
LCD = I2C_LCD_driver.lcd()

instance = dht11.DHT11(pin = 21)

bot = telegram.Bot(token = '6681318558:AAGAEHoLOZKDWbPyY2CrQ5M5nxx61uutQyQ')
chat_id = '754298459'

def keypad_loop(acc):
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    old_X, old_Y, old_Z = acc.get_3_axis_adjusted()
    start_time = time.time()
  
    while True:
        for i in range(3):
            GPIO.output(LED_COL[i], 0)
            for j in range(4):
                if GPIO.input(LED_ROW[j]) == 0:
                    if LED_MATRIX[j][i] == 1:
                        if time.time() - start_time < 10:
                            GPIO.output(24, 0)
                            GPIO.output(18, 0)
                    
                    if LED_MATRIX[j][i] == 2:
                        async def send_message():
                            await bot.send_message(chat_id = chat_id, text = 'Help me!')

                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(send_message())

                    while GPIO.input(LED_ROW[j]) == 0:
                        time.sleep(0.1)

            GPIO.output(LED_COL[i], 1)

        new_X, new_Y, new_Z = acc.get_3_axis_adjusted()

        if (GPIO.output(18) == 0) or (GPIO.output(24) == 0) or (((new_X - old_X) >= abs(1)) or ((new_Y - old_Y) >= abs(1)) or ((new_Z - old_Z) >= abs(1))):
            async def send_message():
                await bot.send_message(chat_id = chat_id, text = 'Help me!')

            loop = asyncio.get_event_loop()
            loop.run_until_complete(send_message())
            GPIO.output(18, 1)
            GPIO.output(24, 1)

if __name__ == '__main__':
    time.sleep(0.5)
    LCD.backlight(0)
    time.sleep(0.5)
    LCD.backlight(1)
    LCD.lcd_display_string('Press 1 to stop alarms', 1, 0)
    LCD.lcd_display_string('Press 2 to call for help', 2, 0)

    for i in range(3):
        GPIO.setup(LED_COL[i], GPIO.OUT)
        GPIO.output(LED_COL[i], 1)

    # Set row pins as inputs, with pull up
    for j in range(4):
        GPIO.setup(LED_ROW[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    acc = adxl345.ADXL345(i2c_port = 1, address = ADDRESS)
    acc.load_calib_value()
    acc.set_data_rate(data_rate = adxl345.DataRate.R_100)
    acc.set_range(g_range=  adxl345.Range.G_16, full_res = True)
    acc.measure_start()

    multiprocessing.Process(target = keypad_loop, args=(acc)).start()

    while True:
        time_strings = time.strftime("%Y,%m,%d,%H,%M,%S")
        time_list = time_strings.split(",")
        time_num = [ int(x) for x in time_list ]
        
        dht_result = instance.read()
        
        print(dht_result.temperature)
        
        if dht_result.is_valid() == False:
            print('Humidity and Temp Sensor not working!')
        
        if dht_result.temperature < 25 or dht_result.temperature > 31:
            async def send_message():
                await bot.send_message(chat_id = chat_id, text = 'Temperature is abnormal!')

            loop = asyncio.get_event_loop()
            loop.run_until_complete(send_message())

        if dht_result.humidity < 40 or dht_result.humidity > 60:
            async def send_message():
                await bot.send_message(chat_id = chat_id, text = 'Humidity is abnormal!')

            loop = asyncio.get_event_loop()
            loop.run_until_complete(send_message())
    
    GPIO.cleanup()
