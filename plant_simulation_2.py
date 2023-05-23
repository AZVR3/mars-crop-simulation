# Plant growth simulation on martian soil
# Assumptions:
# - The plants are grown in a controlled environment with optimal temperature, humidity and light conditions
# - The plants are watered regularly with a nutrient solution
# - The martian soil is mixed with organic matter and fertilizers to improve its quality
# - The plant growth is measured by biomass (dry weight) and height
# - The plant growth is affected by the soil pH, nitrogen, phosphorus and potassium levels

# Import libraries
import numpy as np
import plotly.express as px  # Import plotly
import pandas as pd

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


# Define functions
def logistic_growth(x, k):
    # Logistic growth function with carrying capacity k
    return k * x / (x + k - x * INIT_BIOMASS / k)


def growth_factor(x, x_opt):
    # Growth factor function based on deviation from optimal value x_opt
    return np.exp(-np.abs(x - x_opt) / x_opt)


def simulate_growth():
    # Simulate the plant growth for each crop over time
    biomass = np.zeros((NUM_CROPS, NUM_DAYS))  # Biomass matrix (kg)
    height = np.zeros((NUM_CROPS, NUM_DAYS))  # Height matrix (m)
    biomass[:, 0] = INIT_BIOMASS  # Initial biomass
    height[:, 0] = INIT_HEIGHT  # Initial height

    for i in range(NUM_CROPS):
        for j in range(1, NUM_DAYS):
            # Update biomass and height based on logistic growth and growth factors
            biomass[i, j] = logistic_growth(biomass[i, j - 1], MAX_BIOMASS[i]) * \
                            growth_factor(soil_ph[i], PH_TOLERANCE[i]) * \
                            growth_factor(soil_n[i], N_TOLERANCE[i]) * \
                            growth_factor(soil_p[i], P_TOLERANCE[i]) * \
                            growth_factor(soil_k[i], K_TOLERANCE[i])
            height[i, j] = logistic_growth(height[i, j - 1], MAX_HEIGHT[i]) * \
                           growth_factor(soil_ph[i], PH_TOLERANCE[i]) * \
                           growth_factor(soil_n[i], N_TOLERANCE[i]) * \
                           growth_factor(soil_p[i], P_TOLERANCE[i]) * \
                           growth_factor(soil_k[i], K_TOLERANCE[i])

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
    fig1 = px.line(df, x="day", y="biomass", color="crop", title="Plant biomass on martian soil")
    fig2 = px.line(df, x="day", y="height", color="crop", title="Plant height on martian soil")

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

# Simulate the plant growth for each crop over time
biomass, height = simulate_growth()

# Plot the results using plotly
plot_results(biomass, height)
