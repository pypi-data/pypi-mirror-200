---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
:tags: [remove-input]

%config InlineBackend.figure_formats = ['svg']

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['animation.frame_format'] = "svg"

import warnings
from matplotlib._api import MatplotlibDeprecationWarning
warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)
```

(quickstart)=

# Quickstart

This page gives a whirlwind introduction to flatspin. Make sure you have [installed flatspin](installation) before you continue.

The best way to get familiar with flatspin, is to play with the simulator in an interactive Python environment.
This guide is written as a [Jupyter notebook](https://jupyter.org/), which you can download and run yourself.
Just click the download link from the top of this page.

Let's get started!

+++

## The flatspin model

The main object in flatspin is the [model](model).
Each model class defines a spin ice *geometry*, which specifies the positions and angles of the spins. 
The {class}`SquareSpinIceClosed <flatspin.model.SquareSpinIceClosed>` class, for instance, creates a square spin ice geometry (with "closed" edges):

```{code-cell} ipython3
from flatspin.model import SquareSpinIceClosed

model = SquareSpinIceClosed()
model.plot();
```

A list of available model classes can be found in the [user guide](model).
Custom geometries may be created by [extending flatspin](extending).

## Model parameters

Properties of the model can be changed through *parameters*, which are passed as keyword arguments to the model class. For instance, we may change the `size` parameter to create a larger spin ice:

```{code-cell} ipython3
model = SquareSpinIceClosed(size=(10,5))
print(f"10x5 square ASI has", model.spin_count, "spins")
model.plot();
```

Note that `size` is geometry-specific: for {class}`SquareSpinIceClosed <flatspin.model.SquareSpinIceClosed>`, the size specifies the number of columns (rows) of horizontal (vertical) magnets.
For {class}`KagomeSpinIce <flatspin.model.KagomeSpinIce>`, the size denotes the number of hexagonal units:

```{code-cell} ipython3
from flatspin.model import KagomeSpinIce
model = KagomeSpinIce(size=(10,5))
print(f"10x5 kagome ASI has", model.spin_count, "spins")
model.plot();
```

Other important parameters include `alpha` (the coupling strength), `hc` (the coercive field), `disorder` (random variations in the coercive fields) and `temperature` (absolute temperature in Kelvin). For a list of available parameters, see {class}`SpinIce <flatspin.model.SpinIce>`.

## Running the model

The primary method for interacting with the model is the *external field*. We set the external field with {func}`set_h_ext() <flatspin.model.SpinIce.set_h_ext>`.

```{code-cell} ipython3
model = SquareSpinIceClosed()
model.set_h_ext([-0.058, -0.058])
```

Next we run the model by calling {func}`relax() <flatspin.model.SpinIce.relax>`, which will flip all spins until equilibrium is reached, i.e., until there are no more flippable spins. {func}`relax() <flatspin.model.SpinIce.relax>` returns the number of spins that were flipped.

```{code-cell} ipython3
flips = model.relax()
print(flips, "spins flipped")
model.plot();
```

We may also flip only a single spin at a time by calling {func}`step() <flatspin.model.SpinIce.step>`. For each call to {func}`step() <flatspin.model.SpinIce.step>`, the spin with the highest "switching energy" will be flipped, and the method returns `True`. If there are no flippable spins, {func}`step() <flatspin.model.SpinIce.step>` returns `False`. Below we use {func}`step() <flatspin.model.SpinIce.step>` to create an animation of the relaxation process.

```{code-cell} ipython3
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Reset system back to the polarized state
model.polarize()

fig, ax = plt.subplots()

def do_steps():
    yield model
    while model.step():
        yield model

def animate(model):
    model.plot(ax=ax, replace=True)
        
anim = FuncAnimation(fig, animate, frames=do_steps(), interval=200, blit=False)
plt.close() # Only show the animation
HTML(anim.to_jshtml())
```

## Hysteresis loops

Often we are interested in some average quantity of the ensemble, such as the total magnetization.

A hysteresis loop is a plot of the total magnetization, projected along the direction of the external field. Below we gradually increase the strength `H` of the external field, applied at some angle `phi`, and record the total magnetization for each field value `H`. We also enable GPU acceleration to speed up the simulation with `use_opencl=True`.
If your system is not set up to use opencl, replace with `use_opencl=False` (this will slow down your simulations significantly).

```{code-cell} ipython3
model = SquareSpinIceClosed(size=(10,10), use_opencl=True)

# H decreases linearly from 0.1 to -0.1, then back to 0.1
H = np.linspace(0.1, -0.1, 500)
H = np.concatenate([H, -H])

# Angle of the external field
phi = np.deg2rad(45)
h_dir = np.array([np.cos(phi), np.sin(phi)])

M_H = []

for h in H:
    model.set_h_ext(h * h_dir)
    model.relax()
    # Magnetization projected along field direction
    m = model.total_magnetization().dot(h_dir)
    M_H.append(m)

plt.plot(H, M_H)
plt.xlabel("H [T]")
plt.ylabel(r"M_H [a.u.]");
```

And here is an animation of the hysteresis loop, where only changes to the state are shown:

```{code-cell} ipython3
# Reset system back to the polarized state
model.polarize()

fig, ax = plt.subplots()

def do_hysteresis():
    yield model
    for h in H:
        model.set_h_ext(h * h_dir)
        if model.relax():
            # Only show frames where any spins flipped
            yield model

def animate(model):
    h = model.h_ext[0].dot(h_dir)
    ax.set_title(f'H = {h:g}')
    model.plot(ax=ax, replace=True)
        
anim = FuncAnimation(fig, animate, frames=do_hysteresis(), interval=200, blit=False)
plt.close() # Only show the animation
HTML(anim.to_jshtml())
```

## Temperature

If we increase the temperature, spins flip more easily due to additional thermal energy. Below we can see how temperature affects the hysteresis loop from earlier. Notice how the hysteresis loop becomes narrower at higher temperatures, as the additional thermal energy causes spins to flip for weaker fields.

```{code-cell} ipython3
model = SquareSpinIceClosed(size=(10,10), m_therm=1e-17, use_opencl=True)

# H, phi and h_dir as before

temperatures = [0, 200, 400, 600]

for T in temperatures:
    M_H = []

    model.polarize()
    model.set_temperature(T)
    for h in H:
        model.set_h_ext(h * h_dir)
        model.relax()
        m = model.total_magnetization().dot(h_dir)
        M_H.append(m)

    plt.plot(H, M_H, label=f"{T} K")

plt.xlabel("H [T]")
plt.ylabel(r"M_H [a.u.]");
plt.legend();
```

## Vertices

Spin ice systems are frequently analyzed in terms of its *vertices*. A *vertex* is defined by the points in the geometry where spins point either in or out. In square spin ice, a vertex is surrounded by four spins. In the example below, the blue dots denote the vertices.

```{code-cell} ipython3
model = SquareSpinIceClosed()
model.plot()
model.plot_vertices();
```

The *vertex type* is defined by the dipolar energy between the spins in the vertex. Below we randomize the spin states of the model, and count the number of different vertex types with {func}`vertex_count() <flatspin.model.SpinIce.vertex_count>`. In the plot, the colors of the dots indicate the vertex type: green for type 1 (lowest energy), blue for type 2, red for type 3 and gray for type 4 (highest energy).

```{code-cell} ipython3
model.randomize(seed=0x9876)
print("Vertex counts:", model.vertex_count())
model.plot()
model.plot_vertices();
```

Another useful visualization is the *vertex magnetization*, which is the net magnetic moment of the spins in each vertex.
Type 1 vertices have zero net moment, and depicted as white (empty) regions in the plot below.

```{code-cell} ipython3
model.plot_vertex_mag();
```

## Large scale patterns

Spin-spin interactions can give rise to large scale patterns in the ensemble.
The emergent behavior is a function of the spin ice geometry.
Square spin ice exhibits **antiferromagnetic domains** with zero net magnetization.
Large scale patterns are easily visible if we plot the vertex magnetization.

Below, we initialize a square spin ice to a random configuration, and "anneal" it to a low energy state.
We cheat a bit and use a very high coupling strength `alpha` to anneal the system without any external field.
For a more physically realistic field-based annealing protocol, see [](examples/anneal_field).

```{code-cell} ipython3
model = SquareSpinIceClosed(size=(25,25), alpha=1.0, init='random', use_opencl=True)
model.relax()
model.plot_vertex_mag();
```

Pinwheel spin ice, on the other hand, favors **ferromagnetic domains** with a positive net magnetization.

```{code-cell} ipython3
from flatspin.model import PinwheelSpinIceDiamond
model = PinwheelSpinIceDiamond(size=(25,25), alpha=1.0, init='random', use_opencl=True)
model.relax()
model.plot_vertex_mag();
```

## Energy

The energy of each spin is derived from the total fields acting on each spin, i.e., the dipolar fields, external fields and thermal fields.
Below we obtain the energy of each spin by calling {func}`energy() <flatspin.model.SpinIce.energy>`. Next we use the energy to color the arrows of each spin in the relaxed pinwheel system from above.
Notice how the spins that are part of the domain walls (the boundaries of the ferromagnetic domains) have higher energy than the spins that are well inside the domains.

```{code-cell} ipython3
E = model.energy()
print("Total energy:", np.sum(E))
quiv = model.plot(C=E, cmap='plasma')
plt.colorbar(quiv);
```

## Ready to learn more?

This has been a quick whirlwind introduction to flatspin.
If you haven't already done so, you are encouraged to download this notebook and play with the code examples yourself.
Just click the download button from the top of this page!

In this short time, we have covered only a small part of the flatspin simulator.
To learn more, head over to the [](userguide) and explore the topics covered.
