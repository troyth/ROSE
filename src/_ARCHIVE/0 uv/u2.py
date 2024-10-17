import numpy as np
import matplotlib.pyplot as plt
import colour
from colour.models import Luv_to_XYZ, XYZ_to_RGB

# Create the grid for the plot
x = np.linspace(-2, 2, 500)
y = np.linspace(-2, 2, 500)
X, Y = np.meshgrid(x, y)

# Calculate radius for each point on the grid
R = np.sqrt(X**2 + Y**2)

# Define the color space within the unit circle
# Colors beyond the unit circle are not plotted
mask = R <= 1

# Create U* (red-green) and V* (yellow-blue) components
U = X[mask]  # X represents the horizontal axis, which we align to red-green
V = Y[mask]  # Y represents the vertical axis, which we align to yellow-blue

# Set a fixed lightness value (L*)
L = 50  # L* value (fixed at 50 for this visualization)

# Calculate chroma (C*) and hue (h_uv) based on U and V
chroma = np.sqrt(U**2 + V**2)  # Chroma is the distance from the origin
hue = np.arctan2(V, U)  # Angle for hue

# Convert chroma and hue to CIELUV (L*, u*, v*)
L_array = np.full_like(chroma, L)
u_array = chroma * np.cos(hue)
v_array = chroma * np.sin(hue)

# Convert CIELUV to XYZ
luv = np.stack((L_array, u_array, v_array), axis=-1)
xyz = np.apply_along_axis(lambda luv_value: Luv_to_XYZ(luv_value), -1, luv)

# Normalize XYZ values to the range [0, 1]
xyz_normalized = xyz / np.max(xyz)

# Convert XYZ to sRGB for plotting
rgb = XYZ_to_RGB(xyz_normalized, colour.RGB_COLOURSPACES['sRGB'], chromatic_adaptation_transform='Bradford')

# Clip RGB values to be in valid range
rgb = np.clip(rgb, 0, 1)

# Prepare an empty plot
plt.figure(figsize=(8, 8))

# Use scatter plot to represent chroma and hue values in CIE LUV space
plt.scatter(X[mask], Y[mask], c=rgb, marker='.', s=1)

# Plot the unit circle boundary
circle = plt.Circle((0, 0), 1, color='black', fill=False, linewidth=1.5)
plt.gca().add_artist(circle)

# Set plot limits and labels
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.xlabel('Red-Green Axis (U*)')
plt.ylabel('Yellow-Blue Axis (V*)')
plt.title('Developmental Color Space (U, Gaia) - CIELChuv using Colour-Science at L* = 50')
plt.gca().set_aspect('equal')

# Show the plot
plt.show()
