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
from numpy.linalg import norm
import matplotlib.pyplot as plt
plt.rcParams['animation.frame_format'] = "svg"
```

(dynamics)=

# Dynamics

As discussed in [](switching), flatspin employs a generalized Stoner-Wohlfarth (GSW) switching model to determine whether a spin will flip its magnetization.
A spin may flip if the **total magnetic field** acting on the spin:

1. is outside of the switching astroid (left hand side of the GSW equation is greater than 1) **and**
2. is oriented in the opposite direction of the spin magnetization ($h_\parallel < 0$)

## Switching energy
The **switching energy** captures both these conditions, and can be calculated with {func}`switching_energy() <flatspin.model.SpinIce.switching_energy>`.
When the switching energy is positive, the total field is outside the astroid (1) and antiparallel to the spin magnetization (2).
The magnitude of the switching energy corresponds to how far the total field is outside the astroid.
A spin may flip if, and only if, the switching energy is positive.
A list of flippable spins can be obtained by calling {func}`flippable() <flatspin.model.SpinIce.flippable>`.

Below we color the spins in a square spin ice by their corresponding switching energies:

```{code-cell} ipython3
from flatspin.model import SquareSpinIceClosed

model = SquareSpinIceClosed()
model.spin[[0, 4, 39]] = -1 # flip spins 0, 4 and 39

print("Flippable spins:", model.flippable())

# Calculate the switching energy
E = model.switching_energy()
E_max = np.max(np.abs(E))
quiv = model.plot(C=E, cmap='coolwarm', clim=(-E_max, E_max))
plt.colorbar(quiv);
```

In the example above, the switching energy was always negative, meaning no spins were flippable.
If we increase the external field, we will see that some spins get a positive switching energy and become flippable.

```{code-cell} ipython3
# Increase the external field
model.set_h_ext([0.2, 0])
print("Flippable spins:", model.flippable())

# Calculate the switching energy
E = model.switching_energy()
E_max = np.max(np.abs(E))
quiv = model.plot(C=E, cmap='coolwarm', clim=(-E_max, E_max))
plt.colorbar(quiv);
```

(dynamics-step)=
## Flipping spins

flatspin employs single spin flip dynamics, where only one spin is flipped at a time.
Calling {func}`step() <flatspin.model.SpinIce.step>` advances the simulation one step by flipping a spin.
The dipolar fields are always recalculated as part of a simulation step, **but the thermal fields are not**.

If there are more than one flippable spin, **the spin with the highest switching energy will flip first**.
This ensures that the spin flip order is completely *deterministic*.

In the animation below we flip one spin at a time, until there are no more flippable spins.
Notice how flipping a spin affects the switching energy of neighboring spins, due to the change in dipolar fields.
Consequently, only 3 spins will actually flip, even though there were 6 flippable spins originally.

```{code-cell} ipython3
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def do_steps():
    yield model
    while model.step():
        yield model

def do_plot(model):
    E = model.switching_energy()
    E_max = np.max(np.abs(E))
    model.plot(C=E, cmap='coolwarm', clim=(-E_max, E_max), ax=ax, replace=True)
        
fig, ax = plt.subplots()
anim = FuncAnimation(fig, do_plot, frames=do_steps(), interval=500, blit=False)
plt.close() # Only show the animation
HTML(anim.to_jshtml())
```

(dynamics-relax)=
## Relaxation

Flipping all spins until there are no more flippable spins is referred to as a *relaxation*, and is the core dynamical process of flatspin.
A simulation is advanced by updating the external and/or thermal fields, and then flipping all flippable spins by calling {func}`relax() <flatspin.model.SpinIce.relax>`.
{func}`relax() <flatspin.model.SpinIce.relax>` will re-sample the thermal fields *once*, before starting to flip spins.
Because the external and thermal fields are held constant during relaxation, the process is guaranteed to terminate.
{func}`relax() <flatspin.model.SpinIce.relax>` returns the number of spins that flipped.

Below we use {func}`relax() <flatspin.model.SpinIce.relax>` to simulate the reversal of a square spin ice by an increasing external field.

```{code-cell} ipython3
# Strength of external field
H = np.linspace(0, 0.1, 100)
# Direction of the external field
phi = np.deg2rad(180+45)
h_dir = np.array([np.cos(phi), np.sin(phi)])

def do_reversal():
    yield model
    for h in H:
        model.set_h_ext(h * h_dir)
        if model.relax():
            # Only show plot when there were spin flips
            yield model

def do_plot(model):
    model.plot(ax=ax, replace=True)
        
fig, ax = plt.subplots()
anim = FuncAnimation(fig, do_plot, frames=do_reversal(), interval=500, blit=False)
plt.close() # Only show the animation
HTML(anim.to_jshtml())
```

If the direction of the external field is fixed (*and there is no thermal field*), the relaxation process is invariant to the resolution of the external field.
In other words, increasing the field strength gradually in 10 steps results in the same sequence of spin flips as increasing the strength in a single step:

```{code-cell} ipython3
# Gradually increase strength of external field in 10 steps
model.polarize()
H = 0.058
for h in np.linspace(0, H, 10):
    model.set_h_ext([-h, -h])
    model.relax()
plt.figure()
plt.title("After 10 field steps")
model.plot()

# Set external field in a single step
model.polarize()
model.set_h_ext([-H, -H])
model.relax()
plt.figure()
plt.title("After 1 field step")
model.plot();
```

## Hysteresis loops

Often we are interested in some average quantity of the ensemble, such as the total magnetization.

A hysteresis loop is a plot of the total magnetization, projected along the direction of the external field. Below we gradually increase the strength `H` of the external field, applied at some angle `phi`, and record the total magnetization for each field value `H`. We also enable GPU acceleration to speed up the simulation with `use_opencl=True`.

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
plt.xlabel("H (mT)")
plt.ylabel(r"M_H (a.u.)");
```

Here is an animation of the hysteresis loop, where changes to the state at each {func}`relax() <flatspin.model.SpinIce.relax>` are shown, omitting steps without change:

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
    model.plot(ax=ax, replace=True)
        
anim = FuncAnimation(fig, animate, frames=do_hysteresis(), interval=200, blit=False)
plt.close() # Only show the animation
HTML(anim.to_jshtml())
```

## Disorder

So far the coercive fields of all spins have been identical.
If we introduce disorder in the coercive fields, the hysteresis loop changes.
Below we can see how disorder causes the reversal process to become more gradual.

```{code-cell} ipython3
for disorder in [0, 0.05, 0.10]:
    model = SquareSpinIceClosed(size=(10,10), use_opencl=True, disorder=disorder)

    # H, phi and h_dir as before
    M_H = []
    for h in H:
        model.set_h_ext(h * h_dir)
        model.relax()
        m = model.total_magnetization().dot(h_dir)
        M_H.append(m)

    plt.plot(H, M_H, label=f"{disorder * 100}% disorder")

plt.xlabel("H (mT)")
plt.ylabel(r"M_H (a.u.)");
plt.legend();
```

## Temperature

If we increase the temperature, spins flip more easily due to additional thermal energy. Below we can see how temperature affects the hysteresis loop from earlier. Notice how the hysteresis loop becomes narrower at higher temperatures, as the additional thermal energy causes spins to flip for weaker fields.

```{code-cell} ipython3
model = SquareSpinIceClosed(size=(10,10), m_therm=.5e-17, use_opencl=True)

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

    plt.plot(H, M_H, label=f"{T}K")

plt.xlabel("H (mT)")
plt.ylabel(r"M_H (a.u.)");
plt.legend();
```
