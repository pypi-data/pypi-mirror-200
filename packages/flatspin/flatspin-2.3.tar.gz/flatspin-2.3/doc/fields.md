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

(fields)=

# Magnetic fields

In flatspin, external fields and temperature are modeled as a combination of magnetic fields.
The total magnetic field affecting each spin is the sum of three types of fields:

1. Dipolar fields from neighboring magnets (`h_dip`)
2. An external field (`h_ext`)
3. A stochastic thermal field (`h_therm`)

Magnetic field vectors can be viewed from two frames of reference:
1. The **global reference frame** `[h_x, h_y]` is the most intuitive, where `h_x` is the horizontal component (from left to right) and `h_y` is the the vertical component (going upwards).
2. In the **local reference frame**, the field is projected along the magnetization direction of each spin, resulting in a vector `[h_par, h_perp]` where `h_par` is the field component which is parallel to the magnetization, and `h_perp` is the perpendicular component. In other words, the local reference frame represents the magnetic field "felt" by each spin. When `h_par` is positive, the field is pushing in the same direction as the magnetization, and when `h_par` is negative, the field is pushing in the opposite direction of the magnetization.

In general, field attributes (such as `h_ext`) are always stored in the global reference frame, while the fields returned by field methods (such as {func}`external_fields() <flatspin.model.SpinIce.external_fields>`) are in the local reference frame.

+++

(fields-dipolar)
## Dipolar fields

Spins are coupled through [dipole-dipole interactions](https://en.wikipedia.org/wiki/Magnetic_dipole%E2%80%93dipole_interaction), and each spin is subject to a magnetic field from all neighboring spins.
These dipolar fields can be calculated using {func}`dipolar_fields() <flatspin.model.SpinIce.dipolar_fields>`, which returns an array of vectors `[h_par, h_perp]` where `h_par` is the parallel component of the dipolar field and `h_perp` is the perpendicular component (local reference frame).

Below the spins are colorized according their `h_par` values.

```{code-cell} ipython3
from flatspin.model import SquareSpinIceClosed

model = SquareSpinIceClosed()
model.spin[[0, 4, 39]] = -1 # flip spins 0, 4 and 39

h_dip = model.dipolar_fields()
quiv = model.plot(C=h_dip[:,0], cmap='coolwarm_r')
plt.colorbar(quiv);
```

The strength of the dipolar fields scale with the parameter `alpha` (the coupling strength): a higher `alpha` results in stronger dipolar fields.

Because the dipole-dipole interaction quickly fades over long distances, flatspin only considers a finite neighborhood when computing dipolar fields. The radius of this neighborhood can be configured with the `neighbor_distance` model parameter. Setting `neighbor_distance=np.inf` results in a global neighborhood, but is computationally costly for large systems.

Below we illustrate how the neighborhood (light red) of the center spin (dark red) changes for different values of `neighbor_distance`.
See also [](examples/neighbor_distance) for a discussion on the effects of neighbor distance.

```{code-cell} ipython3
:tags: [hide-input]

plt.figure(figsize=(8,4))
for nd in [1, 2, 3]:
    plt.subplot(1,3,nd)
    plt.title(f'neighbor_distance={nd}')
    m = SquareSpinIceClosed(size=(6,6), neighbor_distance=nd)
    i = m.spin_count//2 - 1
    neighs = np.zeros(m.spin_count)
    neighs[i] = 1
    neighs[m.neighbors(i)] = 0.8
    m.plot(C=neighs, cmap='coolwarm', clim=(0,1))
```

(fields-external)=
## External fields

The external magnetic field is the primary mechanism for altering the state of an ASI in a controlled manner.
To set the external field, use {func}`set_h_ext() <flatspin.model.SpinIce.set_h_ext>`.
The external field can be set either globally for the entire system, or locally on a per spin basis.
The `h_ext` attribute stores the external fields for all the spins (global reference frame).

As with the dipolar fields, the parallel and perpendicular components of the external field acting on each spin can be calculated using {func}`external_fields() <flatspin.model.SpinIce.external_fields>`.

Passing a single vector to {func}`set_h_ext() <flatspin.model.SpinIce.set_h_ext>` sets a global field:

```{code-cell} ipython3
from flatspin.plotting import plot_vectors

# Global external field
model.set_h_ext([0.1, 0.1])

plt.figure()
plt.title("h_ext")
plot_vectors(model.pos, model.h_ext, normalize=True)

plt.figure()
plt.title("h_ext_par")

h_ext = model.external_fields()

# Colorize spins by the parallel component of the external field
quiv = model.plot(C=h_ext[:,0], cmap='coolwarm_r')
plt.colorbar(quiv);
```

Passing an array of vectors to {func}`set_h_ext() <flatspin.model.SpinIce.set_h_ext>` sets a local external field, i.e., an individual external field for each spin.
The length of the array must match the number of spins in the system.

```{code-cell} ipython3
# A local field which increases in strength with spin index
H = np.linspace(0, 0.1, model.spin_count)
phi = np.deg2rad(10)
h_ext = np.column_stack([H * np.cos(phi), H * np.sin(phi)])
print(f'h_ext.shape: {h_ext.shape}')
model.set_h_ext(h_ext)

plt.figure()
plt.title("h_ext")
plot_vectors(model.pos, model.h_ext, normalize=True)

plt.figure()
plt.title("h_ext_par")

h_ext = model.external_fields()

# Colorize spins by the parallel component of the external field
quiv = model.plot(C=h_ext[:,0], cmap='coolwarm_r')
plt.colorbar(quiv);
```

(fields:spatial)=
It is also possible to map a spatial vector field defined on a grid, onto the spins with {func}`set_h_ext_grid() <flatspin.model.SpinIce.set_h_ext_grid>`:

```{code-cell} ipython3
# A spatial vector field defined on a grid
x = np.linspace(0, 2*np.pi, 9, endpoint=True)
y = np.linspace(0, 2*np.pi, 9, endpoint=True)
xx, yy = np.meshgrid(x, y)
H = np.cos(xx) + np.cos(yy)
h_ext = np.stack([0.01*H, 0.1*H], axis=-1)
print(f'h_ext.shape: {h_ext.shape}')

model.set_h_ext_grid(h_ext)

plt.figure()
plt.title("H")
plt.imshow(H, cmap='coolwarm_r')
plt.colorbar()

plt.figure()
plt.title("h_ext")
plot_vectors(model.pos, model.h_ext, normalize=True);
```

(fields-thermal)=
## Thermal fields

The thermal field is a stochastic field which represents thermal fluctuations acting independently on each spin. In most cases, the thermal fields will be directed antiparallel to the spin magnetization, i.e., towards the easiest switching direction (see also [](switching)).

After the temperature is set with {func}`set_temperature() <flatspin.model.SpinIce.set_temperature>`, the thermal field must be re-sampled using {func}`update_thermal_noise() <flatspin.model.SpinIce.update_thermal_noise>`:

```{code-cell} ipython3
# Set temperature to 300 K, and re-sample h_therm
model.set_temperature(300)
model.update_thermal_noise()

plt.title("h_therm @ 300 K")
h_therm_magnitude = norm(model.h_therm, axis=-1)
# Colorize vectors by their magnitude
quiv = plot_vectors(model.pos, model.h_therm,
                    C=h_therm_magnitude, cmap='coolwarm', normalize=True)
plt.colorbar(quiv);
```

Increasing the temperature increases the magnitude of `h_therm` (but does not change the direction):

```{code-cell} ipython3
model.set_temperature(600)
model.update_thermal_noise()

plt.title("h_therm @ 600 K")
h_therm_magnitude = norm(model.h_therm, axis=-1)
# Colorize vectors by their magnitude
quiv = plot_vectors(model.pos, model.h_therm,
                    C=h_therm_magnitude, cmap='coolwarm', normalize=True)
plt.colorbar(quiv);
```

## Total field

Finally, the total magnetic fields are the sum of the dipolar, external and thermal fields. The total field for each spin can be computed directly using {func}`total_fields() <flatspin.model.SpinIce.total_fields>`:

```{code-cell} ipython3
plt.figure()
plt.title("h_tot_par")

h_tot = model.total_fields()

# Colorize spins by the parallel component of the total field
quiv = model.plot(C=h_tot[:,0], cmap='coolwarm_r')
plt.colorbar(quiv);
```

## GPU acceleration

flatspin provides GPU acceleration to speed up calculations of the magnetic fields. Enabling GPU acceleration with `use_opencl=True` can greatly speed up calculations, especially for large systems:

```{code-cell} ipython3
model_cpu = SquareSpinIceClosed(size=(100,100))
%timeit model_cpu.dipolar_fields()
```

```{code-cell} ipython3
model_gpu = SquareSpinIceClosed(size=(100,100), use_opencl=True)
%timeit model_gpu.dipolar_fields()
```
