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
```

(theory)=

# Theory

Please see our paper {cite}`Flatspin2022` for details about the magnetic model implemented by flatspin:

[“flatspin: A Large-Scale Artificial Spin Ice Simulator”, Phys. Rev. B 106, 064408 (2022).](https://doi.org/10.1103/PhysRevB.106.064408)

A short summary is provided below, as well as some additional practical information.

## Magnets as dipoles

:::{figure} _static/dipoles.svg
:alt: dipoles
:::

As illustrated in the above figure, magnets are modelled as magnetic dipoles with *binary* magnetization, i.e., macro spins:

$$
s_i \in \{-1, +1\}
$$

Each magnetic dipole has an associated position $\vec{r}_i$ and rotation $\theta_i$.
Using reduced units, the magnetization vector of a single magnet can be expressed as

$$
\vec{m}_i=s_i \vec{\hat{m}}_i
$$

where $\vec{\hat{m}}_i$ is the unit vector along $\vec{m}_i$.

## Magnetic Fields and Temperature

External fields and temperature are modeled as a combination of effective magnetic fields.
The total field, $\vec{h}_i$, affecting each magnet $i$ is the sum of three components:

$$
\vec{h}_i = \vec{h}_{dip}^{(i)} + \vec{h}_{ext}^{(i)} + \vec{h}_{th}^{(i)}
$$

where $\vec{h}_\text{dip}^{(i)}$ is the local magnetic field from neighboring magnets (magnetic dipole-dipole interactions), $\vec{h}_\text{ext}^{(i)}$ is a global or local external field, and $\vec{h}_\text{th}^{(i)}$ is a random magnetic field representing thermal fluctuations in each magnetic element.

## Magnetic dipole-dipole interactions

Spins are coupled through [dipole-dipole interactions](https://en.wikipedia.org/wiki/Magnetic_dipole%E2%80%93dipole_interaction).
Each spin, $i$, is subject to a magnetic field from all neighboring spins, $j\neq i$, given by

$$
\vec{h}_\text{dip}^{(i)} = \alpha \sum_{j \ne i}\frac{3\vec{r}_{ij}(\vec{m}_j \cdot \vec{r}_{ij})}{|\vec{r}_{ij}|^5} - \frac{\vec{m}_j}{|\vec{r}_{ij}|^3},
$$

where $\vec{r}_{ij}=\vec{p}_i-\vec{p}_j$ is the distance vector from spin $i$ to $j$ and $\alpha$ scales the dipolar coupling strength between spins.
The coupling strength $\alpha$ is given by $\alpha = \frac{\mu_0 M}{4\pi a^3}$, where $a$ is the lattice spacing, $M$ is the net magnetic moment of a single magnet, and $\mu_0$ is the vacuum permeability.
The distance $\vec{r}_{ij}$ is given in reduced units of the lattice spacing.
The size of the neighborhood is user-configurable and defined in units of the lattice spacing.

## External field

Applying an external magnetic field is the primary mechanism for altering the state of an ASI in a controlled manner.
The external field can either be set locally on a per-spin basis, $\vec{h}_\text{ext}^{(i)}$, globally for the entire system, $\vec{h}_\text{ext}$, or as a spatial vector field, $\vec{h}_\text{ext}(\vec{r})$.

Time-dependent external fields are supported, i.e., $\vec{h}_\text{ext}$ is a discrete time series of either local, global or spatial fields.
A variety of time-dependent external fields are provided, including sinusoidal, sawtooth and rotational fields.
More complex field-protocols can be generated, e.g., for annealing purposes or probing dynamic response.

## Thermal field

Thermal fluctuations are modelled as an additional local field, $\vec{h}_\text{th}^{(i)}$, applied to each magnet individually.

The magnitude of the thermal fields, $\vec{h}_\text{th}^{(i)}$, is sampled from a Poisson distribution given by the CDF,

$$
P(X \leq \Delta h) = \exp(-f\Delta t)
$$

where $\Delta h$ is the smallest additional field required for switching, $\Delta t$ is the experimental time interval, and $f$ is the characteristic switching rate given by the Arrhenius-Néel equation,

$$
f = f_0 \exp\left(-\frac{\Delta E}{k_\text{B}T}\right)
  = f_0 \exp\left(-\frac{\Delta h M_\text{th}}{k_\text{B}T}\right),
$$

where $f_0$ is the attempt frequency and $\Delta E$ is the energy barrier for switching.
The energy barrier corresponds to the additional Zeeman energy required for magnetization reversal, i.e., $\Delta E = \Delta h M_\text{th}$, where $M_\text{th}$ is the thermal nucleation moment.

The direction of the thermal vector fields is chosen to take the path of least resistance, i.e., the switching direction with the minimum energy.
In other words, the thermal fields point towards the shortest distance out of the switching astroid.

It is important to note that flatspin does not account for the temperature dependence of the material parameters.
If these parameters are expected to vary significantly in the temperature range of interest, e.g., $M_\text{th}$, this has to be explicitly accounted for by the user.

## Switching

Magnetization reversal, or *switching*, may take place when a magnet is subjected to a magnetic field or high temperature.
If the field is sufficiently strong (stronger than some critical field) and directed so that the projection onto $\vec{m}_i$ is in the opposite direction to $\vec{m}_i$, the magnetization $\vec{m}_i$ will switch direction.

The critical field strength is referred to as the coercive field $\vec{h}_\text{c}$, which depends on the angle between the applied field $\vec{h}_i$ and $\vec{m}_i$.
The external field can be decomposed into two components, $\vec{h}_\parallel$ and $\vec{h}_\perp$, corresponding to the field component parallel and perpendicular to the easy axis, respectively.
We denote the coercive field strength along the hard axis as $h_k$.

flatspin uses a generalized Stoner-Wohlfarth (SW) switching model to allow an asymmetry between easy and hard axes.
The critical field is described by the equation:

$$
\left(\frac{h_{\parallel}}{b h_k}\right)^{2/\gamma} + \left(\frac{h_{\perp}}{c h_k}\right)^{2/\beta} = 1
$$

$b$, $c$, $\beta$ and $\gamma$ are parameters which adjust the shape of the switching astroid: $b$ and $c$ define the height and width, respectively, while $\beta$ and $\gamma$ adjust the curvature of the astroid at the easy and hard axis, respectively.
With $b = c = 1$ and $\beta = \gamma = 3$, the classical Stoner-Wohlfarth astroid is obtained (valid for elliptical magnets).
The plot below illustrates how the parameters affect the shape of the switching astroid:

```{code-cell} ipython3
:tags: [remove-input]

def GSW(h_par, h_perp, b=1, c=1, beta=3, gamma=3):
    """ Generalized Stoner-Wohlfarth astroid  """
    sw = b*(1 - ((h_perp/c)**2)**(1/beta))**(gamma/2)
    sw[h_par<0] *= -1
    return sw

def plot_GSW(b=1, c=1, beta=3, gamma=3, ax=None, **kwargs):
    thetas = np.linspace(0, 2*np.pi, 3601)

    h_perp = c * np.cos(thetas)
    h_par = b * np.sin(thetas)

    kwargs.setdefault("label", rf"$b={b:g}, c={c:g}, \beta={beta:g}, \gamma={gamma:g}$")

    if ax is None:
        ax = plt.gca()
    ax.plot(h_perp, GSW(h_par, h_perp, b, c, beta, gamma), **kwargs)

plot_GSW(label="Stoner-Wohlfarth")
plot_GSW(b=0.5)
plot_GSW(b=0.5, beta=1.5)
plt.xlabel('$h_\perp / h_k$')
plt.ylabel('$h_\parallel / h_k$')
plt.axis('square')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0));
```

In flatspin, the generalized SW model is used as the switching criteria, i.e., a spin may flip if the left hand side of the above equation is greater than one.
Additionaly, the projection of $\vec{h}_\text{i}$ onto $\vec{m}_i$ must be in the opposite direction of $\vec{m}_i$:

$$
\vec{h}_i \cdot \vec{m}_i < 0.
$$

## Imperfections and disorder

Variations in each magnet are modelled as a disorder in the coercive fields.
A user-defined parameter, $k_\text{disorder}$, defines the distribution of coercive fields, i.e., $h_{k}^{(i)}$ is sampled from a normal distribution $\mathcal{N}(h_{k}, \sigma)$, where $\sigma = k_\text{disorder} \cdot h_k$.

## Dynamics

flatspin employs deterministic single spin flip dynamics.
At each simulation step, we calculate the total magnetic field, $\vec{h}_i$, acting on each spin.
Next, we determine which spins *may* flip according to the switching criteria above.
Finally we flip the spin where $\vec{h}_i$ is the furthest outside its switching astroid, i.e., where the left hand side of the SW equation is greatest.
Ties are broken in a deterministic, arbitrary manner, although with non-zero disorder such occurrences are rare.
The above process is repeated until there are no more flippable spins.

This relaxation process is performed with constant external and thermal fields.
To advance the simulation, the fields are updated and relaxation is performed again.
**Hence a simulation run consists of a sequence of field updates and relaxation processes.**

## Geometries

The particular spatial arrangement of the magnets is referred to as the *geometry*.
flatspin includes the most commonly used ASI geometries:  square, kagome, pinwheel and ising.

flatspin can be used to model any two-dimensional ASI comprised of identical elements.
New geometries can easily be added by extending the model with a new set of positions $\vec{r}_i$ and rotations $\theta_i$.

## Parameter and variable listing

The following table lists model parameters with their equivalents in the Python code:

| Parameter           | Python parameter | Description                                |
| ------------------- | ---------------- | ------------------------------------------ |
| $\alpha$            | `alpha`          | Dipolar coupling strength                  |
| $h_k$               | `hc`             | Mean coercive field (along hard axis)      |
| $k_\text{disorder}$ | `disorder`       | Disorder in coercive fields                |
| $b$                 | `sw_b`           | Height of switching astroid (easy axis)    |
| $c$                 | `sw_c`           | Width of switching astroid (hard axis)     |
| $\beta$             | `sw_beta`        | Curvature of switching astroid (easy axis) |
| $\gamma$            | `sw_gamma`       | Curvature of switching astroid (hard axis) |
| $T$                 | `temperature`    | Temperature                                |
| $\Delta t$          | `therm_timescale`| Thermal time scale (seconds per timestep)  |
| $M_\text{th}$       | `m_therm`        | Thermal nucleation moment                  |
| $f_0$               | `attempt_freq`   | Attempt frequency                          |

Additional parameters in the Python code include:

| Python parameter    | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| `size`              | Size of ASI (geometry specific)                               |
| `lattice_spacing`   | Spacing between each spin (in reduced units)                  |
| `neighbor_distance` | Neighborhood to consider when calculating dipole interactions |

The following table lists model variables with their equivalents in the Python code:

| Variable              | Python name        | Description                             |
| --------------------- | ------------------ | --------------------------------------- |
| $s_i$                 | `spin[i]`          | Magnet spin                             |
| $\vec{r}_i$           | `pos[i]`           | Magnet position                         |
| $\theta_i$            | `angle[i]`         | Magnet angle                            |
| $\vec{m}_i$           | `vectors[i]`       | Magnet magnetization                    |
| $h_k^{(i)}$           | `hc[i]`            | Magnet coercive field (along hard axis) |
| $\vec{h}_i$           | `total_field(i)`   | Total magnetic field                    |
| $\vec{h}_{dip}^{(i)}$ | `dipolar_field(i)` | Magnetic field from neighboring magnets |
| $\vec{h}_{ext}^{(i)}$ | `h_ext[i]`         | External magnetic field                 |
| $\vec{h}_{th}^{(i)}$  | `h_therm[i]`       | Thermal field                           |

## Choosing parameters

Here we give some advice on how to set some of the parameters.

### Coupling parameters $\alpha$ and lattice spacing

Although `alpha` defines the lattice spacing between magnets, it is also possible to change the lattice spacing via the `lattice_spacing` parameter.
This has the effect of scaling the magnetic coupling as if changing lattice spacing directly.
A neat trick is to calculate `alpha` based on a lattice spacing of 1 nm, set `lattice_spacing=L` to obtain an effective lattice spacing of `L` nm.
Hence `lattice_spacing` allows setting the lattice spacing directly, e.g., for sweeps, as opposed to indirectly through `alpha`.

### Note on units

The physical unit of the $\vec{h}$-field in flatspin is Tesla $\mathrm{[T]}$.
While the $\vec{H}$-field is typically described in units of $\mathrm{[Am^{-1}]}$, the fields in flatspin are exclusively external to the magnets.
In other words, the $\vec{h}$-field is equivalent to a $\vec{B}$-field in the absence of material magnetization, i.e., $\vec{h} = \mu_0 \vec{H}$. 
Correspondingly, the magnetic moments $M$ and $M_\text{th}$ have units $\mathrm{[Am^2]}$.

### Switching parameters $h_k$, $b$, $c$, $\beta$ and $\gamma$

These parameters define the switching characteristic of the magnets.
They can be estimated from micromagnetic simulations of a single magnet, when subject to a gradually increasing external field at different angles.

Here we provide a list some example magnet sizes corresponding switching parameters:

| Magnet shape | Magnet size   | $h_k$ | $b$  | $c$ | $\beta$ | $\gamma$ |
| ------------ | ------------- | ----- | ---- | --- | ------- | -------- |
| Elliptical   | 220x80x10 nm  | 0.2   | 0.77 | 1.0 | 2.2     | 4.2      |
| Stadium      | 220x80x25 nm  | 0.2   | 0.38 | 1.0 | 1.3     | 3.6      |
| Stadium      | 220x80x20 nm  | 0.2   | 0.41 | 1.0 | 1.5     | 3.9      |
| Stadium      | 470x170x10 nm | 0.14  | 0.28 | 1.0 | 4.8     | 3.0      |
