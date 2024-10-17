import numpy as np
import colorsys
import logging
import plotly.graph_objs as go
import plotly.io as pio

# Configure logging to use a similar font style
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate 3D horn torus data
def generate_3d_horn_torus(resolution=100, radius=1, saturation=1.0):
    logging.info("Generating 3D horn torus with resolution %d and radius %f.", resolution, radius)
    # Create a grid of points in polar coordinates
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, 2 * np.pi, resolution)
    U, V = np.meshgrid(u, v)

    # Apply a phase shift to make V=0 correspond to the center of the torus (singularity)
    X = (radius + radius * np.cos(V + np.pi)) * np.cos(U)
    Y = (radius + radius * np.cos(V + np.pi)) * np.sin(U)
    Z = radius * np.sin(V + np.pi)

    # Opacity determined by v(t), with value ranging from 0 (at center) to 1 (outermost point)
    Opacity = (1 - V / (2 * np.pi)) * (1 - V / (2 * np.pi))

    # Convert hue and saturation to RGB values
    hue = U / (2 * np.pi)
    lightness = 0.5  # Fixed lightness for vibrant colors

    rgb = np.zeros((resolution, resolution, 4))
    for i in range(resolution):
        for j in range(resolution):
            if j == 0:  # Log alpha values for the first longitudinal line
                logging.debug(f"Longitude {i}, Opacity (Alpha): {Opacity[i, j]:.2f}")
            r, g, b = colorsys.hls_to_rgb(hue[i, j], lightness, saturation)
            alpha = Opacity[i, j]  # Keep alpha between 0 and 1 for Plotly
            rgb[i, j] = [r, g, b, alpha]

    return X, Y, Z, rgb

# Function to render the horn tori using Plotly
def render_horn_torus_plotly(resolution=100):
    logging.info("Starting to render the 3D horn tori color space interactively with Plotly.")
    # Generate outer horn torus
    X_outer, Y_outer, Z_outer, colors_outer = generate_3d_horn_torus(resolution, radius=1, saturation=1.0)
    # Generate inner horn torus with 50% radius and less saturation
    X_inner, Y_inner, Z_inner, colors_inner = generate_3d_horn_torus(resolution, radius=0.5, saturation=0.5)

    # Flatten the arrays for Plotly (outer torus)
    x_outer = X_outer.ravel()
    y_outer = Y_outer.ravel()
    z_outer = Z_outer.ravel()
    rgba_colors_outer = colors_outer.reshape(-1, 4)

    # Convert RGB and alpha values to a format that Plotly accepts (hex format) for outer torus
    plotly_colors_outer = [
        f'rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, {alpha})'
        for r, g, b, alpha in rgba_colors_outer
    ]

    # Create hover text with RGBA values for outer torus
    hover_text_outer = [
        f'R: {int(r*255)}, G: {int(g*255)}, B: {int(b*255)}, A: {alpha:.2f}'
        for r, g, b, alpha in rgba_colors_outer
    ]

    # Create a Scatter3d plot with Plotly for outer torus
    trace_outer = go.Scatter3d(
        x=x_outer,
        y=y_outer,
        z=z_outer,
        mode='markers',
        marker=dict(
            size=5,
            color=plotly_colors_outer,  # Set color using RGBA values
        ),
        text=hover_text_outer,  # Add hover text
        hoverinfo='text'  # Display custom text on hover
    )

    # Flatten the arrays for Plotly (inner torus)
    x_inner = X_inner.ravel()
    y_inner = Y_inner.ravel()
    z_inner = Z_inner.ravel()
    rgba_colors_inner = colors_inner.reshape(-1, 4)

    # Convert RGB and alpha values to a format that Plotly accepts (hex format) for inner torus
    plotly_colors_inner = [
        f'rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, {alpha})'
        for r, g, b, alpha in rgba_colors_inner
    ]

    # Create hover text with RGBA values for inner torus
    hover_text_inner = [
        f'R: {int(r*255)}, G: {int(g*255)}, B: {int(b*255)}, A: {alpha:.2f}'
        for r, g, b, alpha in rgba_colors_inner
    ]

    # Create a Scatter3d plot with Plotly for inner torus
    trace_inner = go.Scatter3d(
        x=x_inner,
        y=y_inner,
        z=z_inner,
        mode='markers',
        marker=dict(
            size=5,
            color=plotly_colors_inner,  # Set color using RGBA values
        ),
        text=hover_text_inner,  # Add hover text
        hoverinfo='text'  # Display custom text on hover
    )

    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis=dict(
                visible=False,
            ),
            yaxis=dict(
                visible=False,
            ),
            zaxis=dict(
                visible=False,
            ),
            bgcolor='#eeeeee',  # Set background color to light grey
        ),
    )

    fig = go.Figure(data=[trace_outer, trace_inner], layout=layout)
    pio.show(fig, renderer='browser')  # Open in the default web browser

if __name__ == "__main__":
    render_horn_torus_plotly(resolution=100)
