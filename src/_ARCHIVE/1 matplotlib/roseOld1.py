import numpy as np
import matplotlib.pyplot as plt
import colorsys
import matplotlib
import logging

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
            # Convert polar coordinates to Cartesian coordinates scaled to the image dimensions
            x = int(center + R[i, j] * np.cos(Theta[i, j]) * scale)
            y = int(center + R[i, j] * np.sin(Theta[i, j]) * scale)
            # Check if the point is within bounds
            if 0 <= x < resolution and 0 <= y < resolution:
                # Map the color from the original image to the circular region
                circle[y, x] = square[i, j]
                # logging.debug(f"Mapped point ({i}, {j}) to Cartesian ({x}, {y}) with color {square[i, j]}.")

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

def render_unit_circle_color_wheel(even_density=False):
    # Generate the HSL color wheel
    logging.info("Starting to render the unit circle color wheel.")
    image = generate_color_square(even_density=even_density)

    # Plot the image using imshow for simplicity
    plt.imshow(image, extent=[-1, 1, -1, 1], origin='lower')
    plt.axis('off')  # Hide the axes
    plt.gca().set_aspect('equal')  # Ensure the circle is not stretched
    plt.title("2D HSL Color Wheel with Saturation Gradient")
    plt.show()
    logging.info("Finished rendering the color wheel.")

if __name__ == "__main__":
    render_unit_circle_color_wheel(even_density=True)
