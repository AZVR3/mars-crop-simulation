import csv
import math

# Define constants for solar radiation data from NASA
SOLAR_FILE = "solar_radiation.csv"  # File name of solar radiation data
SOLAR_YEAR = 669  # Number of sols in one Martian year
SOLAR_MIN = 136  # Minimum solar radiation in W/m^2 at Mars aphelion
SOLAR_MAX = 717  # Maximum solar radiation in W/m^2 at Mars perihelion


# Define a function to calculate the solar radiation for a given sol
def solar_radiation(sol):
    # Use a sinusoidal function with amplitude (SOLAR_MAX - SOLAR_MIN) / 2 and period SOLAR_YEAR
    return (SOLAR_MAX + SOLAR_MIN) / 2 + (SOLAR_MAX - SOLAR_MIN) / 2 * math.sin(2 * math.pi * sol / SOLAR_YEAR)


# Open the file in write mode
with open(SOLAR_FILE, "w") as f:
    # Create a csv writer object
    writer = csv.writer(f)

    # Write the header row with column names
    writer.writerow(["Sol", "Solar Radiation"])

    # Loop through each sol from 0 to SOLAR_YEAR - 1
    for sol in range(SOLAR_YEAR):
        # Write a row with the sol number and the solar radiation value
        writer.writerow([sol, solar_radiation(sol)])
