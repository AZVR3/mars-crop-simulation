# Plant Growth Simulator on Mars
import plotly.graph_objects as go  # Import plotly library
import plotly.subplots as ps  # Import plotly subplots library

# Define some constants
MARS_GRAVITY = 3.711  # m/s^2
MARS_ATMOSPHERE = 0.006  # bar
MARS_TEMPERATURE = -63  # C
WATER_CONTENT = 0.05  # fraction of soil mass
NUTRIENT_CONTENT = 0.02  # fraction of soil mass
SUNLIGHT_INTENSITY = 590  # W/m^2
PLANT_GROWTH_RATE = 0.005  # fraction of biomass per day
PLANT_WATER_USE = 0.0005  # fraction of biomass per day
PLANT_NUTRIENT_USE = 0.00005  # fraction of biomass per day


# Define a class for plants
class Plant:
    def __init__(self, name, mass):
        self.name = name
        self.mass = mass  # kg
        self.height = 0.1  # m
        self.alive = True

    def grow(self):
        # Calculate the growth factor based on environmental conditions
        growth_factor = (MARS_GRAVITY / 9.81) * (MARS_ATMOSPHERE / 1) * (MARS_TEMPERATURE + 273) / 300 * (
                SUNLIGHT_INTENSITY / 1000)
        # Update the mass and height of the plant
        self.mass += self.mass * PLANT_GROWTH_RATE * growth_factor
        self.height += self.height * PLANT_GROWTH_RATE * growth_factor

    def use_resources(self):
        global WATER_CONTENT, NUTRIENT_CONTENT
        # Calculate the water and nutrient use of the plant
        water_use = self.mass * PLANT_WATER_USE
        nutrient_use = self.mass * PLANT_NUTRIENT_USE
        # Update the water and nutrient content of the soil
        WATER_CONTENT -= water_use / 1000  # kg -> m^3
        NUTRIENT_CONTENT -= nutrient_use / 1000  # kg -> m^3
        # Check if the plant has enough resources to survive
        if WATER_CONTENT < 0 or NUTRIENT_CONTENT < 0:
            self.alive = False

    def show_status(self):
        # Print the name, mass, height and alive status of the plant
        print(f"{self.name}: mass = {self.mass:.2f} kg, height = {self.height:.2f} m, alive = {self.alive}")


# Create a list of plants
plants = [Plant("Potato", 0.1), Plant("Tomato", 0.05), Plant("Cactus", 0.02), Plant("lettuce", 0.3)]

# Create empty lists to store the data for plotting
days = []
potato_masses = []
tomato_masses = []
cactus_masses = []
lettuce_masses = []
water_contents = []
nutrient_contents = []

# Simulate for 100 days
for day in range(1, 101):
    print(f"Day {day}")
    for plant in plants:
        plant.grow()
        plant.use_resources()
        plant.show_status()
        print(f"Water content = {WATER_CONTENT:.4f} m^3/kg")
        print(f"Nutrient content = {NUTRIENT_CONTENT:.4f} m^3/kg")
        print()
        # Append the data to the lists
        days.append(day)
        potato_masses.append(plants[0].mass)
        tomato_masses.append(plants[1].mass)
        cactus_masses.append(plants[2].mass)
        lettuce_masses.append(plants[3].mass)
        water_contents.append(WATER_CONTENT)
        nutrient_contents.append(NUTRIENT_CONTENT)

# Create a figure with four subplots: one for each plant mass and one for soil resources
fig = ps.make_subplots(rows=3, cols=2, shared_xaxes=True,
                       subplot_titles=["Potato", "Tomato", "Cactus", "Lettuce", "Water Resources", "Nutrient Resources"])

# Add traces for plant masses in the first three subplots
fig.add_trace(go.Scatter(x=days, y=potato_masses, name="Potato", mode="lines+markers"), row=1, col=1)
fig.add_trace(go.Scatter(x=days, y=tomato_masses, name="Tomato", mode="lines+markers"), row=1, col=2)
fig.add_trace(go.Scatter(x=days, y=cactus_masses, name="Cactus", mode="lines+markers"), row=2, col=1)
fig.add_trace(go.Scatter(x=days, y=lettuce_masses, name="Lettuce", mode="lines+markers"), row=2, col=2)

# Add traces for soil resources in the fourth subplot
fig.add_trace(go.Scatter(x=days, y=water_contents, name="Water", mode="lines+markers"), row=3, col=1)
fig.add_trace(go.Scatter(x=days, y=nutrient_contents, name="Nutrient", mode="lines+markers"), row=3, col=2)

# Update the layout of the figure to show the y-axis titles and adjust the margins
fig.update_layout(
    yaxis=dict(title="Plant Mass (kg)"),
    yaxis2=dict(title="Plant Mass (kg)"),
    yaxis3=dict(title="Plant Mass (kg)"),
    yaxis4=dict(title="Water Resource (m^3/kg)"),
    yaxis5=dict(title="Nutrient Resource (m^3/kg)"),
    margin=dict(l=20, r=20, t=50, b=20)
)

# Show the figure in the output
fig.show()
