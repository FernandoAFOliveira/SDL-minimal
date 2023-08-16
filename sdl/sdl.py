import logging
import serial
import time
import os
from pathlib import Path
from datetime import datetime, timedelta

#Create a system log directory and files
LOG_DIRECTORY = "system_logs"
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)    
current_time = datetime.utcnow()
log_filename = current_time.strftime("log_%Y_%m_%d_%H_%M_%S.log")
LOG_FILE_PATH = os.path.join(LOG_DIRECTORY, log_filename)
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Script started")

# Setting up custom logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)


# SETTINGS
PORT_NUMBER = "COM8"
BAUD_RATE = 9600
LOG_DIRECTORY = "Emulated-data_logs"

# Connect to the serial port
try:
    ser = serial.Serial(PORT_NUMBER, BAUD_RATE, timeout=1)
    ser.flush()
except serial.SerialException:
    logger.error(f"Unable to connect to port {PORT_NUMBER}. Please check the port and try again.")
    exit()

# Ensure the logging directory exists
log_dir_path = Path(LOG_DIRECTORY)
log_dir_path.mkdir(parents=True, exist_ok=True)

def get_file_name(dt):
    return f"data-log-UTC-{dt.strftime('%Y-%m-%d-%H-%M')}.csv"

def wait_for_next_minute():
    current_time = datetime.utcnow()
    while current_time.second != 0:  # Wait until the start of a new minute
        logger.info(f"Waiting... Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
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
                logger.info(f"Data received: {line} at {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                log_file.write(f"\t{line}")
                log_file.flush()

# Test log
wait_for_next_minute()
test_start_time = datetime.utcnow().replace(second=0, microsecond=0)
logger.info(f"Starting test log to: {get_file_name(test_start_time)}")
start_logging_for_duration(test_start_time, timedelta(minutes=1))
logger.info(f"Test log successful. Data written to file: {log_dir_path / get_file_name(test_start_time)}")

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
    logger.info(f"Starting log: {get_file_name(hour_start)}")
    start_logging_for_duration(hour_start, duration)
    logger.info(f"Log saved to directory: {log_dir_path / get_file_name(hour_start)}")
    
logger.info(f"Finished successfully")