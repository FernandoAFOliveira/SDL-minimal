import serial
import time
import random

def generate_random_number():
    """Generate a random number between 0 and 1023."""
    return random.randint(0, 1023)

def send_random_data_to_serial(port, baudrate=9600, timeout=1, interval=1):
    """Send random data to a specified serial port at given intervals."""
    with serial.Serial(port, baudrate, timeout=timeout) as ser:
        while True:
            data = str(generate_random_number()) + '\n'  # Convert number to string and add a newline
            ser.write(data.encode('utf-8'))  # Encoding the string to bytes
            print(f"Sent: {data}")
            time.sleep(interval)

if __name__ == "__main__":
    PORT = "COM7"  # The port where you want to send data
    send_random_data_to_serial(PORT)
