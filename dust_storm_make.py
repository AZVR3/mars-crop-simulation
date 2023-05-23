import csv
import math
import random

# Define constants for dust storm data from NASA
DUST_FILE = "dust_storm.csv"  # File name of dust storm data
DUST_YEAR = 669  # Number of sols in one Martian year
DUST_MIN = 0.01  # Minimum dust opacity at Mars clear sky
DUST_MAX = 9.9  # Maximum dust opacity at Mars global dust storm


# Define a function to calculate the dust opacity for a given sol
def dust_storm(sol):
    # Use a random number generator to simulate the occurrence and intensity of dust storms
    # Assume that dust storms are more likely and severe in the southern hemisphere summer
    # Use a sinusoidal function with amplitude 0.5 and period DUST_YEAR to model the seasonal variation
    # Add a random noise term to introduce some variability
    return DUST_MIN + (DUST_MAX - DUST_MIN) * (
                0.5 + 0.5 * math.sin(2 * math.pi * sol / DUST_YEAR) + random.uniform(-0.1, 0.1))


# Open the file in write mode
with open(DUST_FILE, "w") as f:
    # Create a csv writer object
    writer = csv.writer(f)

    # Write the header row with column names
    writer.writerow(["Sol", "Dust Opacity"])

    # Loop through each sol from 0 to DUST_YEAR - 1
    for sol in range(DUST_YEAR):
        # Write a row with the sol number and the dust opacity value
        writer.writerow([sol, dust_storm(sol)])
