import numpy as np
import matplotlib.pyplot as plt
import colorsys
import matplotlib
import logging
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

    # Parametric equations for the horn torus (where both radii are the same)
    X = (R + R * np.cos(V)) * np.cos(U)
    Y = (R + R * np.cos(V)) * np.sin(U)
    Z = R * np.sin(V)

    # Opacity determined by v(t)
    Opacity = V / (2 * np.pi)  # Normalized opacity from 1 (opaque) to 0 (transparent)

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
            alpha = Opacity[i, j]
            rgb[i, j] = [r, g, b, alpha]

    return X, Y, Z, rgb

def render_horn_torus_3d(resolution=100, even_density=False, camera_position=None):
    # Generate the horn torus color space
    logging.info("Starting to render the 3D horn torus color space.")
    X, Y, Z, colors = generate_3d_horn_torus(resolution, even_density)

    # Plot the 3D horn torus
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, facecolors=colors, rstride=1, cstride=1, antialiased=True)

    # Set the camera position if provided
    if camera_position is not None:
        ax.view_init(elev=camera_position[0], azim=camera_position[1])

    ax.set_title("3D Horn Torus Color Space")
    ax.set_axis_off()

    # Let matplotlib automatically adjust axis limits for better perspective
    ax.set_box_aspect([1, 1, 1])  # Ensure equal scaling on all axes to avoid distortion

    plt.show()
    logging.info("Finished rendering the horn torus.")

if __name__ == "__main__":
    render_horn_torus_3d(resolution=100, even_density=True, camera_position=(45, 60))
