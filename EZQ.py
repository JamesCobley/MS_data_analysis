import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Standard concentrations (in mg/mL) and corresponding signal values
concentrations = np.array([10, 5, 2.5, 1.25, 0.625, 0.312, 0.156, 0.0781])
signals = np.array([49256, 39995, 22967, 11465, 4617, 2561, 684, 537])  # Example signals

# Define a quadratic function for the fit: y = ax^2 + bx + c
def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

# Perform curve fitting with the quadratic model
params, _ = curve_fit(quadratic, concentrations, signals)
a, b, c = params

# Calculate the fitted values and R²
fitted_signals = quadratic(concentrations, *params)
ss_res = np.sum((signals - fitted_signals) ** 2)  # Sum of squares of residuals
ss_tot = np.sum((signals - np.mean(signals)) ** 2)  # Total sum of squares
r_squared = 1 - (ss_res / ss_tot)  # R² value

# Print the fitted parameters and R²
print(f"Fitted parameters: a={a:.6f}, b={b:.6f}, c={c:.6f}")
print(f"R² value of the fit: {r_squared:.4f}")

# Plot the standard curve and fitted quadratic model
plt.figure(figsize=(8, 6))
plt.scatter(concentrations, signals, color="blue", label="Standards (data points)")
plt.plot(concentrations, fitted_signals, color="red", label="Fitted quadratic curve")
plt.title("Standard Curve: Signal vs. Concentration")
plt.xlabel("Concentration (mg/mL)")
plt.ylabel("Signal")
plt.legend()
plt.grid()
plt.show()

# Function to calculate concentration from signal using the quadratic equation
def calculate_concentration(signal_value):
    # Ensure the signal value is within the range of standard signals
    if signal_value < min(signals) or signal_value > max(signals):
        return None  # Signal out of range

    # Solve the quadratic equation: ax^2 + bx + c - signal = 0
    coefficients = [a, b, c - signal_value]  # Adjust c to include -signal
    roots = np.roots(coefficients)  # Solve for x
    # Only consider the positive root
    positive_root = [root for root in roots if np.isreal(root) and root > 0]
    return positive_root[0].real if positive_root else None  # Return the valid root

# Array of unknown signal values (replace with your actual data)
unknown_signals = np.array([32967, 33728, 27714, 40390])  # Example signals for unknowns

# Calculate concentrations for all unknowns
unknown_concentrations_mg_per_ml = [calculate_concentration(signal) for signal in unknown_signals]

# Print the results
print("\nResults for unknown samples:")
for i, (signal, concentration) in enumerate(zip(unknown_signals, unknown_concentrations_mg_per_ml), 1):
    if concentration is not None:
        # Convert concentration from mg/mL to µg/mL
        concentration_ug_per_ml = concentration * 1000  # µg/mL

        # Example: Calculate volume to obtain 100 ng of protein
        target_amount_ng = 100  # Target amount in ng
        volume_ul = (target_amount_ng / 1000) / concentration * 1000  # µL

        print(f"Unknown sample {i}:")
        print(f"  Signal = {signal}")
        print(f"  Concentration = {concentration:.4f} mg/mL")
        print(f"  Concentration = {concentration_ug_per_ml:.4f} µg/mL")
        print(f"  Volume to load for 100 ng = {volume_ul:.2f} µL")
    else:
        print(f"Unknown sample {i}: Signal = {signal}, Concentration could not be determined (out of range)")
