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

(model)=

# The model object

In this chapter we will get familiar with the flatspin model object, which implements the [theoretical model](theory).
We will cover how to create a model object, setting parameters, and different model attributes.

This guide is written as a [Jupyter notebook](https://jupyter.org/), which can be downloaded by clicking the download link from the top of the page.

+++

The main object in flatspin is the *model* ({mod}`flatspin.model`). Each model class defines a spin ice *geometry*, which specifies the positions and angles of the spins. The {class}`SquareSpinIceClosed <flatspin.model.SquareSpinIceClosed>` class, for instance, creates a square spin ice geometry (with "closed" edges):

```{code-cell} ipython3
from flatspin.model import SquareSpinIceClosed

model = SquareSpinIceClosed()
model.plot();
```

flatspin comes with model classes for some common geometries, shown in the gallery below:

```{code-cell} ipython3
:tags: [hide-input]

import flatspin.model

class_names = ['SquareSpinIceClosed', 'SquareSpinIceOpen',
               'KagomeSpinIce', 'KagomeSpinIceRotated',
               'PinwheelSpinIceDiamond', 'PinwheelSpinIceLuckyKnot',
              ]

n_cols = 3
n_rows = int(np.ceil(len(class_names) / n_cols))
plt.figure(figsize=(2*n_cols, 2*n_rows))
for i, name in enumerate(class_names):
    cls = getattr(flatspin.model, name)
    plt.subplot(n_rows, n_cols, i+1)
    plt.title(name)
    model = cls()
    model.plot()
    plt.axis(False)
plt.tight_layout(w_pad=8)
```

If you would like to add your own geometries, see [](extending).

(model-params)=
## Model parameters

Properties of the model can be changed through *parameters*, which are passed as keyword arguments to the model class. Note that the model *only* accepts keyword arguments (and no positional arguments).

For example, we may change the `size` parameter to create a larger spin ice:

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

+++

(model-spin)=
## Dealing with spins

The state of all the spins is stored in the `spin` array. Spin values are either `1` or `-1`, and are all initialized to `1` at model instantiation.

```{code-cell} ipython3
model = SquareSpinIceClosed()
model.spin
```

You may access elements of this array directly to read or modify the state of spins.
Alternatively, use {func}`flip() <flatspin.model.SpinIce.flip>` to flip a single spin, {func}`set_spin() <flatspin.model.SpinIce.set_spin>` to set the state of all spins, or {func}`polarize() <flatspin.model.SpinIce.polarize>` to reset all spins to `1` or `-1`.

```{code-cell} ipython3
model.spin[0] = -1
model.spin[-1] = -1
model.flip(4)
model.plot();
```

The `spin` array has a flat index, where spins are ordered sequentially. Sometimes it can be easier to work in a different coordinate system, which is where spin labels come in. The left plot below shows the index of each spin. The right plot shows the corresponding labels, for {class}`SquareSpinIceClosed <flatspin.model.SquareSpinIceClosed>`, which uses a `(row, col)` labeling scheme.

```{code-cell} ipython3
:tags: [hide-input]

plt.figure(figsize=(8,4))
plt.subplot(121)
plt.title("Spin indices")
model.plot()
for i in model.indices():
    plt.text(model.pos[i,0], model.pos[i,1], str(i), ha='center', va='center')

plt.subplot(122)
plt.title("Spin labels")
model.plot()
for i, l in enumerate(model.labels):
    plt.text(model.pos[i,0], model.pos[i,1], tuple(l), ha='center', va='center')
```

You can use the `L` object to look up the spin index of a label, or a label range:

```{code-cell} ipython3
L = model.L
print("(4,2):", L[4,2])
print("Row 3:", L[3])
print("Column 4:", L[:,4])
print("Rows 1-3:", L[1:4])
print("Odd rows:", L[1::2])
```

(model-geometry)=
## Geometry

Spin ice geometry is defined by the positions and angles of all the spins, and are stored in the `pos` and `angle` attributes. Positions are in reduced units, defined by `alpha` (see [](theory)). The angles are in radians and define the rotation for the spins *assuming a positive spin value of `1`*.

Please note that these attributes are considered **read-only** and cannot be changed after model initialization.

```{code-cell} ipython3
print(f"Spin 0 has position {model.pos[0]} and angle {np.rad2deg(model.angle[0])}")
print(f"Spin 4 has position {model.pos[4]} and angle {np.rad2deg(model.angle[4])}")
```

As an alternative to tuning the coupling strength `alpha`, the distance between spins may be adjusted by the `lattice_spacing` parameter. This affects the positions of the spins directly, as opposed to indirectly through `alpha` (see [](theory)).

```{code-cell} ipython3
model2 = SquareSpinIceClosed(lattice_spacing=10)
# Notice change in x/y labels when we plot()
model2.plot();
```

(model-vectors)=
## Magnetization vectors

As mentioned above, `angle` is independent of the current spin state. To obtain the magnetization direction, use {attr}`vectors <flatpsin.model.SpinIce.vectors>`.

```{code-cell} ipython3
print(f"Spin 0 has magnetization {model.vectors[0]}")
print(f"Spin 1 has magnetization {model.vectors[1]}")
print(f"Spin 4 has magnetization {model.vectors[4]}")
```

(model-hc)=
## Coercive fields and disorder

The coercive field defines the critical field strength required to flip a spin (see also [](switching)). 
The coercive fields for all spins are stored in the `threshold` array of the model object.
By default, the coercive fields are uniformly set to the parameter `hc`.
We can introduce small variations in the coercive fields by setting the `disorder` parameter, in which case the thresholds are sampled from a normal distribution with mean `hc` and standard deviation `disorder * hc`.

Below we plot a histogram of the coercive fields with 1% and 5% disorder.

```{code-cell} ipython3
model1 = SquareSpinIceClosed(size=(25,25), hc=0.1, disorder=0.01)
model5 = SquareSpinIceClosed(size=(25,25), hc=0.1, disorder=0.05)
bins = np.linspace(0.08, 0.12, 21) - 0.001
plt.hist(model1.threshold, bins=bins, label='1% disorder', alpha=0.5)
plt.hist(model5.threshold, bins=bins, label='5% disorder', alpha=0.5)
plt.legend()
plt.xlabel("hc");
```

## GPU acceleration

flatspin provides GPU acceleration to speed up calculations on the GPU, but note that this must be explicitly enabled by setting the parameter `use_opencl=True`. It is primarily the calculations of the magnetic fields that benefit from running on the GPU.
