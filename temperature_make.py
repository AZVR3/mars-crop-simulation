import csv
import math

# Define constants for temperature data from NASA
TEMP_FILE = "temperature.csv"  # File name of temperature data
TEMP_YEAR = 669  # Number of sols in one Martian year
TEMP_MIN = -143  # Minimum temperature in C at Mars poles
TEMP_MAX = 35  # Maximum temperature in C at Mars equator


# Define a function to calculate the temperature for a given sol and hour
def temperature(sol, hour):
    # Use a sinusoidal function with amplitude (TEMP_MAX - TEMP_MIN) / 2 and period 24 hours
    # Shift the phase by 12 hours to match the peak temperature at noon
    return (TEMP_MAX + TEMP_MIN) / 2 + (TEMP_MAX - TEMP_MIN) / 2 * math.sin(2 * math.pi * (hour - 12) / 24)


# Open the file in write mode
with open(TEMP_FILE, "w") as f:
    # Create a csv writer object
    writer = csv.writer(f)

    # Write the header row with column names
    writer.writerow(["Sol", "Hour", "Temperature"])

    # Loop through each sol from 0 to TEMP_YEAR - 1
    for sol in range(TEMP_YEAR):
        # Loop through each hour from 0 to 23
        for hour in range(24):
            # Write a row with the sol number, the hour, and the temperature value
            writer.writerow([sol, hour, temperature(sol, hour)])
