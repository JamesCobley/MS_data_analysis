import numpy as np
from scipy.optimize import curve_fit

# Standard concentrations (in µg/mL) and corresponding signal values
concentrations = np.array([1000, 500, 250, 125, 62.5, 31.25, 15.625, 7.8125])
signals = np.array([152356, 96111, 54385, 29341, 15467, 8487, 4237, 2156])

# Define a linear function for fitting without an intercept (b = 0)
def linear_no_intercept(x, m):
    return m * x

# Perform the curve fitting using a linear model without an intercept
params, _ = curve_fit(linear_no_intercept, concentrations, signals)
m = params[0]

# Calculate the fitted values and R²
fitted_signals = linear_no_intercept(concentrations, *params)
ss_res = np.sum((signals - fitted_signals) ** 2)  # Sum of squares of residuals
ss_tot = np.sum((signals - np.mean(signals)) ** 2)  # Total sum of squares
r_squared = 1 - (ss_res / ss_tot)  # R² value
print(f"Fitted parameter: m={m}")
print(f"R² value of the fit: {r_squared:.4f}")

# Function to calculate concentration for an array of unknowns
def calculate_concentrations(signal_values):
    concentrations = []
    for signal_value in signal_values:
        # Solve the linear equation m * x = signal for x (concentration)
        concentration = signal_value / m
        concentrations.append(concentration)
    return concentrations

# Array of unknown signal values
unknown_signals = np.array([140925, 10214])  # Replace with actual unknown signal values

# Calculate concentrations for all unknowns
unknown_concentrations = calculate_concentrations(unknown_signals)

# Calculate volume required to obtain 100 ng of peptide for each unknown
target_amount_ng = 100  # Target amount in ng

print("\nResults for unknown samples:")
for i, (signal, concentration) in enumerate(zip(unknown_signals, unknown_concentrations), 1):
    if concentration is not None:
        # Convert concentration from µg/mL to µg/µL
        concentration_ug_per_ul = concentration / 1000  # µg/µL

        # Calculate the volume in µL required to obtain 100 ng of peptide
        volume_ul = (target_amount_ng / 1000) / concentration * 1000  # µL

        print(f"Unknown sample {i}:")
        print(f"  Signal = {signal}")
        print(f"  Concentration = {concentration:.4f} µg/mL")
        print(f"  Concentration in µg/µL = {concentration_ug_per_ul:.6f} µg/µL")
        print(f"  Volume to load for 100 ng = {volume_ul:.2f} µL")
    else:
        print(f"Unknown sample {i}: Signal = {signal}, Concentration could not be determined")
