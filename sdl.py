import serial
import time
from pathlib import Path
from datetime import datetime, timedelta

# SETTINGS
PORT_NUMBER = "COM3"
BAUD_RATE = 9600
LOG_DIRECTORY = "data_logs"

# Connect to the serial port
try:
    ser = serial.Serial(PORT_NUMBER, BAUD_RATE, timeout=1)
    ser.flush()
except serial.SerialException:
    print(f"Unable to connect to port {PORT_NUMBER}. Please check the port and try again.")
    exit()

# Ensure the logging directory exists
log_dir_path = Path(LOG_DIRECTORY)
log_dir_path.mkdir(parents=True, exist_ok=True)

def get_file_name(dt):
    return f"data-log-UTC-{dt.strftime('%Y-%m-%d-%H-%M')}.csv"

def wait_for_next_minute():
    current_time = datetime.utcnow()
    while current_time.second != 0:  # Wait until the start of a new minute
        print(f"Waiting... Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        time.sleep(1)  # Wait for 1 second
        current_time = datetime.utcnow()  # Update the current time

def write_header(file):
    seconds_headers = "\t".join([f"{i:02d}" for i in range(60)])
    file.write(f"Minutes\\Seconds\t{seconds_headers}\n")

def start_logging_for_duration(start_time, duration):
    with open(log_dir_path / get_file_name(start_time), 'w') as log_file:
        write_header(log_file)
        end_time = start_time + duration
        current_minute = start_time.minute
        while datetime.utcnow() < end_time:
            current_time = datetime.utcnow()
            if current_time.minute != current_minute:
                current_minute = current_time.minute
                log_file.write(f"\n{current_time.strftime('%H:%M')}")
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                current_time = datetime.utcnow()
                print(f"Data received: {line} at {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                log_file.write(f"\t{line}")
                log_file.flush()

# Test log
wait_for_next_minute()
test_start_time = datetime.utcnow().replace(second=0, microsecond=0)
print(f"Starting test log to: {get_file_name(test_start_time)}")
start_logging_for_duration(test_start_time, timedelta(minutes=1))
print(f"Test log successful. Data written to file: {log_dir_path / get_file_name(test_start_time)}")

# Continuous logging
first_log = True
while True:
    # For the very first log, start at the current minute, for all other logs, start at the top of the hour
    if first_log:
        hour_start = datetime.utcnow().replace(second=0, microsecond=0)
        first_log = False
    else:
        hour_start = (datetime.utcnow() + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    
    duration = timedelta(hours=1) - timedelta(minutes=hour_start.minute)
    print(f"Starting log: {get_file_name(hour_start)}")
    start_logging_for_duration(hour_start, duration)
    print(f"Log saved to directory: {log_dir_path / get_file_name(hour_start)}")
