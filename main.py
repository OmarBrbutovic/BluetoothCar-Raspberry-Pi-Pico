# This code controls a car using UART communication and an ultrasonic sensor.
# The car can move in all directions and stop based on commands received via the UART channel over Bluetooth.
# The car has a crash prevention feature that uses the ultrasonic sensor to detect obstacles in front of the robot.
# If the crash prevention feature is enabled and the car is about to collide with an obstacle, the robot will stop.
# The car has a function to measure the distance to an obstacle using the ultrasonic sensor.

from machine import Pin, PWM, UART  # importing PIN, PWM and UART
import utime  # importing utime

# Define UART channel and set baud rate to 9600
uart = UART(0, 9600)

# Define pins for control of the DC motors
In1 = Pin(6, Pin.OUT)  # IN1 -> GPIO6(PIN9)
In2 = Pin(7, Pin.OUT)  # IN2 -> GPIO7(PIN10)
In3 = Pin(4, Pin.OUT)  # IN3 -> GPIO4(PIN6)
In4 = Pin(3, Pin.OUT)  # IN4 -> GPIO3(PIN5)

# Define PWM channels for the enable pins of the DC motors
EN_A = PWM(Pin(8))  # ENA -> GPIO8(PIN11)
EN_B = PWM(Pin(2))  # ENB -> GPIO2(PIN4)
# Set the frequency for the PWM signals on the enable pins to 1500 Hz
EN_A.freq(1500)
EN_B.freq(1500)
# Set the duty cycle of the PWM signals on the enable pins to 65025, which is the maximum value
# This will set the speed of the DC motors to their maximum
EN_A.duty_u16(65025)
EN_B.duty_u16(65025)

# Define pins for control of the ultrasonic sensor
trigger = Pin(21, Pin.OUT)  # triger -> GPIO21
echo = Pin(20, Pin.IN)  # echo -> GPIO20

# Set crash prevention default value to True and turn on the LED
crash_prevention = True
LED = Pin(25, Pin.OUT)
LED.high()

# Define function to measure distance using ultrasonic sensor


def ultra():
    # Trigger the ultrasonic sensor by setting trigger low for 2 us, then high for 5 us, then low again
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    # Measure the time it takes for the echo to go from low to high
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    # Measure the time it takes for the echo to go from high to low
    while echo.value() == 1:
        signalon = utime.ticks_us()
    # Calculate the time it took for the echo to go from low to high and back to low
    timepassed = signalon - signaloff
    # Calculate the distance based on the speed of sound and the time it took for the echo to go from low to high and back to low
    distance = (timepassed * 0.0343) / 2
    print(distance)
    # If crash prevention is enabled, check if the distance is less than 20 cm and stop if it is
    if (crash_prevention == True):
        if (distance < 20):
            if ('backward' in data):
                move_backward()  # Backward
            else:
                stop()

    return distance
# ---------------------------------------------------------
# Define function to move the robot forward


def move_forward():
    In1.high()
    In2.low()
    In3.low()
    In4.high()

# Define function to move the robot backward


def move_backward():
    In1.low()
    In2.high()
    In3.high()
    In4.low()

# Define function to stop the robot


def stop():
    In1.low()
    In2.low()
    In3.low()
    In4.low()

# Define function to turn the robot right


def turn_right():
    In1.low()
    In2.high()
    In3.low()
    In4.high()

# Define function to turn the robot left


def turn_left():
    In1.high()
    In2.low()
    In3.high()
    In4.low()
# ---------------------------------------------------------
# Define function to turn the robot slightly right forward


def slight_right():
    In1.low()
    In2.low()
    In3.low()
    In4.high()

# Define function to turn the robot slightly left forward


def slight_left():
    In1.high()
    In2.low()
    In3.low()
    In4.low()

# Define function to turn the robot slightly right backwards


def backward_right():
    In1.high()
    In2.high()
    In3.high()
    In4.low()

# Define function to turn the robot slightly left backwards


def backward_left():
    In1.low()
    In2.high()
    In3.high()
    In4.high()
# ---------------------------------------------------------


data = ""  # Initialize data to an empty string

while True:
    dist = ultra()  # Measure the distance and set dist to the result
    if uart.any():  # Check if there is any data available on the UART channel
        data = uart.read()  # Getting data
        data = str(data)  # Converting bytes to str type
        print(data)

        if ('HC-SR04_ON' in data):
            crash_prevention = True
            LED.high()
        elif ('HC-SR04_OFF' in data):
            crash_prevention = False
            LED.low()
        else:
            pass

        if ('forward' in data):
            move_forward()
        elif ('backward' in data):
            move_backward()
        elif ('right' in data):
            turn_right()
        elif ('left' in data):
            turn_left()
        elif ('upRight' in data):
            slight_right()
        elif ('upLeft' in data):
            slight_left()
        elif ('downRight' in data):
            backward_right()
        elif ('downLeft' in data):
            backward_left()
        elif ('stop' in data):
            stop()
        elif ('E' in data):
            speed = data.split("|")
            print(speed[1])
            # Calculate the duty cycle based on the speed received and set the duty cycle of EN_A and EN_B to the calculated value
            set_speed = float(speed[1])/100 * 65025
            EN_A.duty_u16(int(set_speed))  # Setting Duty Cycle
            EN_B.duty_u16(int(set_speed))  # Setting Duty Cycle
        else:
            stop()  # Stop
