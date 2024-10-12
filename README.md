# ROSE WINDOW
ROSE WINDOW is a Horn Torus color space combining developmental and alchemical dynamics in one 3D domain. These two systems are interpreted as two dimensions of the Earth: Gaia and Sophia. The ROSE WINDOW is a means of mapping the Heros Journey of the Earth.

![Developmental and Alchemical Plane Diagrams](/images/u_v.png)

![Developmental-Alchemical Space](/images/uv.png)

## Developmental Plane (U, Gaia)
The developmental plane, U, is both perceptual and infinite. It is based on the opponent model of human vision, making a 2D chroma plane out of two orthogonal axes that range from Red to Green and Yellow to Blue.

The values of 1 or -1 on each axis corresponds to pure colors of full saturation. For example, the value of 1 on the Red-Green axis is pure red.

Thus, the plane features a chromatic unit circle that ranges from full saturation at its edge to colorless grey in the center. Beyond this unit circle are conceptual colors that we call Platonic.

The infinite plane can be thought of as bounded by Platonic Red, Platonic Green, Platonic Yellow, and Platonic Blue.

## Alchemical Plane (V, Sophia)
The alchemical plane is derived from a conceptual point Sun projecting a full spectrum of frequencies through a 2D prism such that the visible spectrum of light is cast precisely onto the face of a 2D Moon.

The result is a circle that has a Face and a Dark Side. The semicircular Face takes on the color gradient of a rainbow. On the Dark Side, just over the horizon from Red is Infrared (IR), and just over the horizon from Violet is Ultra Violet (UV).

Directly opposite the Sun is the Inner Sun, which rests on the surface of the 2D Moon. This point forms a singularity and is labled as Negative Green (-G), as it lies opposite Green on the Face. Between -G and IR is White, and between -G and UV is Black.

The alchemical color plane has 12 colors but one is a singularity, a point, so the 2D Moon has arcs that take on one of 11 colors. Each arc is a gradient (ie. the orange arc will have different color values along it, ranging from redder to more yellow) except for White and Black, which are pure white and pure black throughout their arc.

The alchemical plane is not a surface but rather hosts a 1D color line curved into a circle. Color is only well-defined along this circle.

## Horn Torus
The two planes, U and V, are orthogonal to each other, with the -G singularity of the alchemical plane being aligned with the center of the developmental plane.

The ROSE WINDOW is created by rotating the alchemical 2D Moon around the unit circle of the developmental plane, forming a Horn Torus. This rotation also causes the point Sun to also rotate, resulting in a radiant outer source circle that inscribes the Horn Torus. At its center is the Inner Sun.

## Path
A path along the surface of the ROSE WINDOW is defined by a Lissajous curve. The two angles, u(t) and v(t), describe the point along the path at a given moment, t, in time.

## Universe
While each plane is defined by color, a point along the surface of the resulting Horn Torus is unable to be reduced to a single color. Instead, it is understood by the coherence of the two colors at that point in each of the two planes.

The principle coherence algorithm is that of harmony. If each of the two colors are thought of as frequencies, then they will produce a repeating pattern if their frequencies are commensurate. In other words, a point at which the two planes are harmonic will produce music. Where they are incommensurate, they will produce non-repeating frequencies, which could be understood as either lyrics or chaos.

Thus, a path through the ROSE WINDOW is a song. Some songs are more beautiful that others.

## Heros Journey
Harmonic Lissajous curves produce a path that begins and ends at the central singularity.

We interpret this center as a worm hole as it resembles a Star from the bottom, where it appears white, and a black hole from the top, where it appears black. Any Lissajous curve that begins at the central singularity and passes from White to Infrared to Red to Orange, Yellow, Green, Blue, Indigo, Violet, Ultra Violet, and finally Black before arriving again at the singularity is defined as a Heros Journey.

A Heros Journey thus travels through the entire spectrum of the alchemical Luni-Solar system but is not constrained by the developmental plane: it may traverse many developmental colors or very few.

## Implementation
The ROSE WINDOW has been implemented in the `src` directory using `mathplotlib` and Python. You can visit [https://rosewindow.fabryx.org/](https://rosewindow.fabryx.org/) to plot Heros Journey paths along the ROSE WINDOW by changing the following parameters:
* radius of the 2D Moon (where <= 0.5 produces a ROSE WINDOW entirely in the perceptual colors and > 0.5 introduces Platonic Colors and > 1 means that each point on a path will always contain either a Platonic color or a color from the Dark Side of the Moon)
* starting and ending u(t) angle (ie. at which developmental altitude the path begins and ends, which corresponds to the degree of wisdom gained)
* the length of the path (which corresponds to the amount of experience that will be converted into wisdom)

## Authorgit config user.email
Created by [Troy Therrien](https://troyth.us).
