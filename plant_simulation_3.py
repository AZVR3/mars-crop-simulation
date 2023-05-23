# Plant growth simulation on martian soil with martian atmosphere
# Assumptions:
# - The plants are grown in a controlled environment with optimal temperature, humidity and light conditions
# - The plants are watered regularly with a nutrient solution
# - The martian soil is mixed with organic matter and fertilizers to improve its quality
# - The plant growth is measured by biomass (dry weight) and height
# - The plant growth is affected by the soil pH, nitrogen, phosphorus and potassium levels
# - The plants are grown in a transparent dome that protects them from the low pressure and radiation, but allows the sunlight and temperature to vary according to the martian seasons
# - The plants are watered regularly with a nutrient solution that contains enough carbon dioxide for photosynthesis
# - The plant growth is affected by the solar radiation, which varies with the distance from the Sun and the dust storms
# - The plant growth is also affected by the temperature, which varies with the latitude, elevation, and time of day

# Import libraries
import numpy as np
import pandas as pd
import datetime as dt
import plotly.express as px  # Import plotly
from scipy.interpolate import interp1d  # Import scipy.interpolate

# Define constants
NUM_DAYS = 100  # Number of days to simulate
NUM_CROPS = 7  # Number of crops to simulate
CROPS = ["potato", "tomato", "lettuce", "radish", "bean", "pepper", "dandelion"]  # Crop names
INIT_BIOMASS = 0.01  # Initial biomass (kg) of each crop
INIT_HEIGHT = 0.1  # Initial height (m) of each crop
MAX_BIOMASS = [1.0, 0.5, 0.2, 0.1, 0.4, 0.3, 0.15]  # Maximum biomass (kg) of each crop
MAX_HEIGHT = [1.0, 2.0, 0.3, 0.2, 1.5, 1.0, 0.5]  # Maximum height (m) of each crop
GROWTH_RATE = [0.02, 0.03, 0.04, 0.05, 0.03, 0.02, 0.01]  # Growth rate (per day) of each crop
PH_TOLERANCE = [6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7]  # Optimal soil pH for each crop
N_TOLERANCE = [150, 150, 150, 150, 200, 150, 100]  # Optimal soil nitrogen (mg/kg) for each crop
P_TOLERANCE = [50, 50, 50, 50, 50, 50, 50]  # Optimal soil phosphorus (mg/kg) for each crop
K_TOLERANCE = [100, 100, 100, 100, 100, 100, 100]  # Optimal soil potassium (mg/kg) for each crop

# Define constants for solar radiation, temperature, and dust storm factors for each crop
SOLAR_FACTOR = [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.4]  # Solar radiation factor for each crop (higher means more sensitive)
TEMP_FACTOR = [1.2, 1.2, 1.4, 1.4, 1.2, 1.2, 1]  # Temperature factor for each crop (higher means more sensitive)
DUST_FACTOR = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.6]  # Dust storm factor for each crop (lower means more sensitive)

# Define constants for latitude, elevation, and time zone of the dome location on Mars
LATITUDE = 18.65  # Latitude in degrees north (positive) or south (negative)
ELEVATION = -4.5  # Elevation in km above or below mean radius of Mars
TIME_ZONE = 3  # Time zone in hours east (positive) or west (negative) of prime meridian

# Define constants for solar radiation data from NASA
SOLAR_FILE = "solar_radiation.csv"  # File name of solar radiation data
SOLAR_YEAR = 669  # Number of sols in one Martian year
SOLAR_MIN = 136  # Minimum solar radiation in W/m^2 at Mars aphelion
SOLAR_MAX = 717  # Maximum solar radiation in W/m^2 at Mars perihelion

# Define constants for temperature data from NASA
TEMP_FILE = "temperature.csv"  # File name of temperature data
TEMP_YEAR = 669  # Number of sols in one Martian year
TEMP_MIN = -143  # Minimum temperature in C at Mars poles
TEMP_MAX = 35  # Maximum temperature in C at Mars equator

# Define constants for dust storm data from NASA
DUST_FILE = "dust_storm.csv"  # File name of dust storm data
DUST_YEAR = 669  # Number of sols in one Martian year
DUST_MIN = 0.01  # Minimum dust opacity at Mars clear sky
DUST_MAX = 9.9  # Maximum dust opacity at Mars global dust storm


# Define functions

def logistic_growth(x, k):
    # Logistic growth function with carrying capacity k
    return k * x / (x + k - x * INIT_BIOMASS / k)


def growth_factor(x, x_opt):
    # Growth factor function based on deviation from optimal value x_opt
    return np.exp(-np.abs(x - x_opt) / x_opt)


def solar_radiation(day):
    # Solar radiation function based on day of Martian year

    # Read solar radiation data from file
    df_solar = pd.read_csv(SOLAR_FILE)

    # Interpolate solar radiation data using linear interpolation
    f_solar = interp1d(df_solar["Day"], df_solar["Solar_Radiation"], kind="linear")

    # Return interpolated solar radiation value for given day
    return f_solar(day)


def temperature(day, hour):
    # Temperature function based on day of Martian year and hour of Martian day

    # Read temperature data from file
    df_temp = pd.read_csv(TEMP_FILE)

    # Interpolate temperature data using linear interpolation
    f_temp = interp1d(df_temp["Day"], df_temp["Temperature"], kind="linear")

    # Calculate diurnal temperature variation based on latitude and elevation
    dtv = 20 * np.cos(np.radians(LATITUDE)) * np.exp(-ELEVATION / 10)

    # Calculate local time based on time zone
    local_time = hour + TIME_ZONE

    # Calculate diurnal temperature factor based on local time
    dft = np.cos(2 * np.pi * local_time / 24)

    # Return interpolated temperature value plus diurnal variation for given day and hour
    return f_temp(day) + dtv * dft


def dust_storm(day):
    # Dust storm function based on day of Martian year

    # Read dust storm data from file
    df_dust = pd.read_csv(DUST_FILE)

    # Interpolate dust storm data using linear interpolation
    f_dust = interp1d(df_dust["Day"], df_dust["Dust_Opacity"], kind="linear")

    # Return interpolated dust opacity value for given day
    return f_dust(day)


def simulate_growth():
    # Simulate the plant growth for each crop over time
    biomass = np.zeros((NUM_CROPS, NUM_DAYS))  # Biomass matrix (kg)
    height = np.zeros((NUM_CROPS, NUM_DAYS))  # Height matrix (m)
    biomass[:, 0] = INIT_BIOMASS  # Initial biomass
    height[:, 0] = INIT_HEIGHT  # Initial height

    # Define the start date of the simulation as the first day of Martian year 36 at noon
    start_date = dt.datetime(2020, 3, 23, 12)

    for i in range(NUM_CROPS):
        for j in range(1, NUM_DAYS):
            # Calculate the current date as the start date plus j sols
            current_date = start_date + dt.timedelta(days=j * 1.0274912517)

            # Calculate the current day of Martian year as the number of sols since the start of the year
            current_day = (current_date.date() - dt.date(current_date.year, 3, 23)).days * 1.0274912517

            # Calculate the current hour of Martian day as the number of hours since midnight
            current_hour = current_date.hour + (current_date.minute + current_date.second / 60) / 60

            # Calculate the solar radiation, temperature, and dust storm effects on plant growth
            solar_effect = solar_radiation(current_day) / SOLAR_MAX * growth_factor(
                solar_radiation(current_day) / (1 + dust_storm(current_day)), SOLAR_FACTOR[i])
            temp_effect = growth_factor(temperature(current_day, current_hour), TEMP_FACTOR[i])
            dust_effect = growth_factor(1 / (1 + dust_storm(current_day)), DUST_FACTOR[i])

            # Update biomass and height based on logistic growth and growth factors
            biomass[i, j] = logistic_growth(biomass[i, j - 1], MAX_BIOMASS[i]) * \
                            growth_factor(soil_ph[i], PH_TOLERANCE[i]) * \
                            growth_factor(soil_n[i], N_TOLERANCE[i]) * \
                            growth_factor(soil_p[i], P_TOLERANCE[i]) * \
                            growth_factor(soil_k[i], K_TOLERANCE[i]) * \
                            solar_effect * temp_effect * dust_effect
            height[i, j] = logistic_growth(height[i, j - 1], MAX_HEIGHT[i]) * \
                           growth_factor(soil_ph[i], PH_TOLERANCE[i]) * \
                           growth_factor(soil_n[i], N_TOLERANCE[i]) * \
                           growth_factor(soil_p[i], P_TOLERANCE[i]) * \
                           growth_factor(soil_k[i], K_TOLERANCE[i]) * \
                           solar_effect * temp_effect * dust_effect

    return biomass, height


def plot_results(biomass, height):
    # Plot the biomass and height results for each crop over time using plotly

    # Create a dataframe with the biomass and height data for each crop and day
    df = pd.DataFrame()
    df["day"] = np.tile(np.arange(NUM_DAYS), NUM_CROPS)
    df["crop"] = np.repeat(CROPS, NUM_DAYS)
    df["biomass"] = biomass.flatten()
    df["height"] = height.flatten()

    # Create line plots for biomass and height using plotly.express
    fig1 = px.line(df, x="day", y="biomass", color="crop",
                   title="Plant biomass on martian soil with martian atmosphere")
    fig2 = px.line(df, x="day", y="height", color="crop", title="Plant height on martian soil with martian atmosphere")

    # Show the plots in the browser
    fig1.show()
    fig2.show()


# Generate random soil parameters for each crop
np.random.seed(42)  # Set random seed for reproducibility
soil_ph = np.random.uniform(5.5, 8.5, size=NUM_CROPS)  # Soil pH (unitless)
soil_n = np.random.uniform(50, 250, size=NUM_CROPS)  # Soil nitrogen (mg/kg)
soil_p = np.random.uniform(10, 90, size=NUM_CROPS)  # Soil phosphorus (mg/kg)
soil_k = np.random.uniform(50, 150, size=NUM_CROPS)  # Soil potassium (mg/kg)

# Print the soil parameters for each crop
print("Soil parameters for each crop:")
print("Crop\t\tpH\tN\tP\tK")
for i in range(NUM_CROPS):
    print(f"{CROPS[i]:<8}\t{soil_ph[i]: .2f}\t{soil_n[i]: .2f}\t{soil_p[i]: .2f}\t{soil_k[i]: .2f}")

# Simulate the plant growth for each crop over time with martian atmosphere
biomass, height = simulate_growth()

# Plot the results using plotly
plot_results(biomass, height)
