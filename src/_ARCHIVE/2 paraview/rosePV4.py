import numpy as np
import matplotlib.pyplot as plt
import colorsys
import matplotlib
import logging
import pyvista as pv
from mpl_toolkits.mplot3d import Axes3D

# Set Matplotlib to use the default system font
matplotlib.rcParams['font.family'] = 'monospace'
matplotlib.rcParams['font.monospace'] = ['Monaco', 'monospace']
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans', 'sans-serif']

# Configure logging to use a similar font style
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('matplotlib').setLevel(logging.WARNING)

def map_square_to_circle(square, Theta, R, resolution):
    # Create a new image array with transparency for the circular region
    circle = np.ones((resolution, resolution, 4)) * [1, 1, 1, 0]  # Initialize to fully transparent

    center = resolution // 2
    scale = resolution / 2

    for i in range(resolution):
        for j in range(resolution):
            if j == 0:  # Log alpha values for the first longitudinal line
                logging.debug(f"Longitude {i}, Opacity (Alpha): {Opacity[i, j]:.2f}")
            # Convert polar coordinates to Cartesian coordinates scaled to the image dimensions
            x = int(center + R[i, j] * np.cos(Theta[i, j]) * scale)
            y = int(center + R[i, j] * np.sin(Theta[i, j]) * scale)
            # Check if the point is within bounds
            if 0 <= x < resolution and 0 <= y < resolution:
                # Map the color from the original image to the circular region
                circle[y, x] = square[i, j]
                logging.debug(f"Mapped point ({i}, {j}) to Cartesian ({x}, {y}) with color {square[i, j]}.")

    return circle

def generate_even_density_r(resolution=500):
    # Generate radius values that are evenly spaced in area
    return np.sqrt(np.linspace(0, 1, resolution))

def generate_color_square(resolution=500, even_density=False):
    # Create a grid of points in polar coordinates
    theta = np.linspace(0, 2 * np.pi, resolution)
    if even_density:
        r = generate_even_density_r(resolution)
    else:
        r = np.linspace(0, 1, resolution)
    Theta, R = np.meshgrid(theta, r)

    logging.info("Generated polar coordinate grid.")

    # Initialize image array with transparency channel
    square = np.ones((resolution, resolution, 4))  # Set to white background with alpha channel

    # Fill the image with colors based on the hue (theta) and saturation (r)
    for i in range(resolution):
        for j in range(resolution):
            hue = Theta[i, j] / (2 * np.pi)
            saturation = R[i, j]
            lightness = 0.5  # Fixed lightness for vibrant colors
            r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
            square[i, j] = [r, g, b, 1.0]  # Set RGB and full opacity
            if i == 0 and j % 100 == 0:  # Log a few sample points to check the process
                logging.debug(f"Pixel ({i}, {j}) - Hue: {hue:.2f}, Saturation: {saturation:.2f}, RGB: ({r:.2f}, {g:.2f}, {b:.2f})")

    return map_square_to_circle(square, Theta, R, resolution)

def generate_3d_horn_torus(resolution=100, even_density=False):
    logging.info("Generating 3D horn torus with resolution %d.", resolution)
    # Create a grid of points in polar coordinates
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, 2 * np.pi, resolution)
    U, V = np.meshgrid(u, v)

    # Radius values (both radii are equal for a horn torus)
    R = 1  # Radius of both the "tube" and the "ring"

    # Apply a phase shift to make V=0 correspond to the center of the torus (singularity)
    X = (R + R * np.cos(V + np.pi)) * np.cos(U)
    Y = (R + R * np.cos(V + np.pi)) * np.sin(U)
    Z = R * np.sin(V + np.pi)

    # Opacity determined by v(t), with value ranging from 0 (at center) to 1 (outermost point)
    Opacity = 1 - V / (2 * np.pi)

    # Convert hue and saturation to RGB values
    hue = U / (2 * np.pi)
    saturation = 1.0  # Full saturation for vibrant colors
    lightness = 0.5  # Fixed lightness for vibrant colors

    rgb = np.zeros((resolution, resolution, 4))
    for i in range(resolution):
        for j in range(resolution):
            if j == 0:  # Log alpha values for the first longitudinal line
                logging.debug(f"Longitude {i}, Opacity (Alpha): {Opacity[i, j]:.2f}")
            r, g, b = colorsys.hls_to_rgb(hue[i, j], lightness, saturation)
            alpha = Opacity[i, j]  # Keep alpha between 0 and 1 for PyVista
            rgb[i, j] = [r, g, b, alpha]

    return X, Y, Z, rgb

def render_horn_torus_pyvista(resolution=100, even_density=False):
    logging.info("Starting to render the 3D horn torus color space interactively.")
    X, Y, Z, colors = generate_3d_horn_torus(resolution, even_density)

    # Flatten the arrays for PyVista
    points = np.c_[X.ravel(), Y.ravel(), Z.ravel()]

    # Create a PyVista PolyData object and set point colors with RGBA values
    mesh = pv.PolyData(points)

    # Extract the RGBA values and ensure opacity is in the range [0, 1]
    rgba_colors = colors.reshape(-1, 4)
    rgba_colors[:, 3] = np.clip(rgba_colors[:, 3], 0, 1)  # Ensure opacity is within range [0, 1]

    mesh.point_data['RGBA'] = rgba_colors

    # Create a PyVista plotter and add the mesh
    plotter = pv.Plotter()

    # Enable transparency blending mode in the plotter
    plotter.enable_depth_peeling()  # Depth peeling helps with better transparency rendering

    # Add the mesh to the plotter with RGBA settings
    plotter.add_mesh(
        mesh,
        scalars='RGBA',
        rgba=True,
        use_transparency=True,
        preference='point'
    )

    plotter.add_axes()
    plotter.show(title='Interactive 3D Horn Torus')

if __name__ == "__main__":
    render_horn_torus_pyvista(resolution=100, even_density=True)
