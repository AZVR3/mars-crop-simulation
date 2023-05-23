# Import some libraries
import numpy as np
import plotly.graph_objects as go  # import plotly instead of matplotlib

# Define some constants
MARS_GRAVITY = 3.711  # m/s^2
MARS_ATMOSPHERE = 0.006  # kPa
MARS_TEMPERATURE = -60  # C
MARS_SOIL = 0.1  # fraction of organic matter
WATER_CONTENT = 0.1  # fraction of water in soil
LIGHT_INTENSITY = 590  # W/m^2
CO2_CONCENTRATION = 0.95  # fraction of CO2 in atmosphere

# Define some plant parameters
# These are based on some assumptions and estimations, not real data
PLANTS = ["potato", "tomato", "radish", "lettuce", "bean", "pepper", "dandelion"]
MASS = [0.1, 0.05, 0.01, 0.02, 0.03, 0.04, 0.02]  # kg
HEIGHT = [0.3, 0.5, 0.1, 0.2, 0.4, 0.3, 0.4]  # m
GROWTH_RATE = [0.005, 0.01, 0.015, 0.02, 0.025, 0.02, 0.015]  # kg/day
WATER_DEMAND = [0.025, 0.05, 0.01, 0.015, 0.02, 0.03, 0.02]  # kg/day
CO2_DEMAND = [0.005, 0.01, 0.005, 0.005, 0.01, 0.01, 0.005]  # kg/day

# Define some simulation parameters
DAYS = 100  # number of days to simulate
DT = 1  # time step in days

# Initialize some variables
mass = np.array(MASS)  # mass of each plant in kg
height = np.array(HEIGHT)  # height of each plant in m
water = WATER_CONTENT * MARS_SOIL * height * np.pi * (height / 2) ** 2  # water available for each plant in kg
co2 = CO2_CONCENTRATION * MARS_ATMOSPHERE * height * np.pi * (height / 2) ** 2  # co2 available for each plant in kg

# Create some lists to store the results
mass_history = []  # list of mass arrays for each day
height_history = []  # list of height arrays for each day
water_history = []  # list of water arrays for each day
co2_history = []  # list of co2 arrays for each day

# Run the simulation loop
for day in range(DAYS):
    # Append the current values to the lists
    mass_history.append(mass)
    height_history.append(height)
    water_history.append(water)
    co2_history.append(co2)

    # Calculate the growth factor for each plant based on the environmental conditions
    # These are some arbitrary functions that depend on light intensity ,temperature ,water and co2 availability
    growth_factor = LIGHT_INTENSITY * np.exp(-((MARS_TEMPERATURE - 20) / 10) ** 2) * np.minimum(
        water / WATER_DEMAND / DT / MASS, co2 / CO2_DEMAND / DT / MASS)

    # Update the mass and height of each plant based on the growth factor and the growth rate
    mass += growth_factor * GROWTH_RATE * DT
    height += growth_factor * GROWTH_RATE * DT / MASS

    # Update the water and co2 availability for each plant based on the water and co2 demand and the soil and atmosphere conditions
    water -= WATER_DEMAND * DT
    water += WATER_CONTENT * MARS_SOIL * height * np.pi * (height / 2) ** 2
    co2 -= CO2_DEMAND * DT
    co2 += CO2_CONCENTRATION * MARS_ATMOSPHERE * height * np.pi * (height / 2) ** 2

# Convert the lists to numpy arrays for easier plotting
mass_history = np.array(mass_history)
height_history = np.array(height_history)
water_history = np.array(water_history)
co2_history = np.array(co2_history)

# Plot the results for each plant using plotly instead of matplotlib
for i in range(len(PLANTS)):
    fig = go.Figure()  # create a figure object using plotly

    # add a trace for mass vs days
    fig.add_trace(go.Scatter(x=list(range(DAYS)), y=mass_history[:,i], name="Mass"))

    # add a trace for height vs days
    fig.add_trace(go.Scatter(x=list(range(DAYS)), y=height_history[:, i], name="Height"))

    # add a trace for water vs days
    fig.add_trace(go.Scatter(x=list(range(DAYS)), y=water_history[:, i], name="Water"))

    # add a trace for co2 vs days
    fig.add_trace(go.Scatter(x=list(range(DAYS)), y=co2_history[:, i], name="CO2"))

    # update the layout with title and axis labels
    fig.update_layout(title=PLANTS[i], xaxis_title="Days", yaxis_title="kg or m")

    fig.show()  # show the figure using plotly
