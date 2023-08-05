---
jupytext:
  formats: ipynb,md:myst
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

# Switching

flatspin uses a generalized Stoner-Wohlfarth (GSW) switching model to describe the angle-dependent switching threshold (coercive field) of a spin.

A *switching astroid* is a polar plot of the coercive field at different angles, with $h_{\perp}$ on the horizontal axis (hard axis) and $h_{\parallel}$ on the vertical axis (easy axis) (see [](fields)).

The coercive field is described by the GSW equation (see [](theory)):

$$
\left(\frac{h_{\parallel}}{b h_k}\right)^{2/\gamma} + \left(\frac{h_{\perp}}{c h_k}\right)^{2/\beta} = 1
$$

The parameters $b$, $c$, $\beta$ and $\gamma$ adjust the shape of the switching astroid: $b$ and $c$ define the height and width, respectively, while $\beta$ and $\gamma$ adjust the curvature of the astroid at the easy and hard axis, respectively.
$h_k$ scales the coercive fields and corresponds to the switching threshold at $h_\parallel=0$, i.e., when the field is aligned with the hard axis.
In the flatspin model, $h_k$ corresponds to the `hc` parameter.

Tuning the parameters of the GSW equation allows the model to capture the switching characteristics of magnets with different shapes.
For example:
* **Elliptical magnets** have a symmetric astroid, described by the regular Stoner-Wohlfarth model: $b=c=1$ and $\beta=\gamma=3$.
* **Rectangular magnets** have an asymmetric switching astroid: they switch more easily along the parallel axis: $b < c$.

Below we plot the GSW astroid for a few different parameters:

```{code-cell} ipython3
:tags: [hide-input]

def GSW(h_par, h_perp, b=1, c=1, beta=3, gamma=3):
    """ Generalized Stoner-Wohlfarth astroid  """
    sw = b*(1 - ((h_perp/c)**2)**(1/beta))**(gamma/2)
    sw[h_par<0] *= -1
    return sw

def plot_GSW(b=1, c=1, beta=3, gamma=3, ax=None, angle_range=(0, 2*np.pi), **kwargs):
    thetas = np.linspace(angle_range[0], angle_range[1], 3601)

    h_perp = c * np.cos(thetas)
    h_par = b * np.sin(thetas)
    
    kwargs.setdefault("label", rf"$b={b:g}, c={c:g}, \beta={beta:g}, \gamma={gamma:g}$")

    if ax is None:
        ax = plt.gca()
    return ax.plot(h_perp, GSW(h_par, h_perp, b, c, beta, gamma), **kwargs)
```

```{code-cell} ipython3
plot_GSW(label="Stoner-Wohlfarth")
plot_GSW(b=0.5)
plot_GSW(b=0.5, beta=1.5)
plt.xlabel('$h_\perp / h_k$')
plt.ylabel('$h_\parallel / h_k$')
plt.axis('square')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0));
```

## Switching a spin

A spin may flip if the total magnetic field acting on the spin:

1. is outside of the switching astroid (left hand side of the GSW equation is greater than 1)
2. is oriented in the opposite direction of the spin magnetization ($h_\parallel < 0$)

To illustrate the switching model, let us consider a single vertical spin:

```{code-cell} ipython3
from flatspin.model import IsingSpinIce

model = IsingSpinIce(size=(1,1))
model.plot();
```

Next, let us set up a cycling external field at some angle to the spin.
The animation below shows the switching astroid for the spin (left plot) with the corresponding magnetic field superimposed (arrow inside the astroid).
The top right column shows the state of the spin, and the bottom right column shows the external field.

Notice how switching only occurs when the field crosses the *negative side* of the astroid ($h_\parallel < 0$), because of switching condition (2).
After switching, the external field is aligned with the magnetization of the spin, and the field arrow jumps to the positive side of the astroid ($h_\parallel > 0).

Because only the negative side of the astroid is relevant for switching, the positive side of the astroid is marked with a dashed line in the astroid plots below.

```{code-cell} ipython3
:tags: [hide-input]

from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from flatspin.encoder import Triangle
from flatspin.plotting import plot_vectors, vector_colors

def animate_switching(model, H=0.15, phi=-100):
    # Reset system back to the polarized state
    model.polarize()
    hk = model.threshold.reshape((-1,1))

    # Set up figure and axes
    fig = plt.figure(facecolor='white')
    ax_astroid = plt.subplot2grid((2,3), (0,0), rowspan=2, colspan=2)
    ax_spin = plt.subplot2grid((2,3), (0,2))
    ax_h_ext = plt.subplot2grid((2,3), (1,2))

    # Set up external field (triangle wave)
    enc = Triangle(timesteps=64, H=H, phi=phi)
    h_ext = enc([1])

    # Plot astroid with field vector
    plt.sca(ax_astroid)
    line, = plot_GSW(*model.sw_params, angle_range=(np.pi, 2*np.pi))
    plot_GSW(*model.sw_params, angle_range=(0, np.pi), ls='dashed', color=line.get_color())
    origin = np.tile([0, 0], (model.spin_count, 1))
    plot_vectors(origin, origin, C=origin[:,0],
                 clim=(-.5,.5), cmap='bwr_r', scale=1, width=.05, pivot='tail', mask_zero=False)
    plt.xlabel('$h_\perp / h_k$')
    plt.ylabel('$h_\parallel / h_k$')

    # spin axis
    plt.sca(ax_spin)
    plt.axis('off')
    plt.title('spin')

    # h_ext axis
    plt.sca(ax_h_ext)
    plt.axis('off')
    plt.title('h_ext')

    def do_cycle():
        for h in h_ext:
            model.set_h_ext(h)
            model.relax()
            h_tot = model.total_fields()
            yield model.total_fields()

    def do_plot(h_tot):
        h_tot /= hk
        h_tot = np.column_stack([h_tot[:,1], h_tot[:,0]])
        plot_vectors(origin, h_tot, C=np.sign(h_tot[:,1]), ax=ax_astroid, replace=True)

        model.plot(ax=ax_spin, replace=True)

        h_ext = model.h_ext / hk
        plot_vectors(model.pos, h_ext, ax=ax_h_ext, replace=True, scale=.5, width=.1)

    anim = FuncAnimation(fig, do_plot, init_func=lambda: None, frames=do_cycle(), interval=200, blit=False)
    plt.close() # Only show the animation
    #anim.save("astroid.gif")
    return HTML(anim.to_jshtml())
```

```{code-cell} ipython3
animate_switching(model)
```

We may change the astroid shape of the spins in the model by setting the parameters `sw_b`, `sw_c`, `sw_beta` and `sw_gamma`.
Below we change switching parameters to describe an elliptical magnet, and repeat the switching animation.
Notice how elliptical magnets are much harder to switch when the field is aligned to the easy axis.

```{code-cell} ipython3
model = IsingSpinIce(size=(1,1), sw_b=1, sw_c=1, sw_beta=3, sw_gamma=3)
animate_switching(model)
```

## Switching many spins

Finally, we illustrate the switching process for a system of coupled spins in a square spin ice.
Inside the astroid, there is one arrow for each spin.
There are two main groups of arrows, since spins have two orientations (horizontal and vertical).
Notice how, within a group, the arrows do not overlap perfectly.
This is because of the dipolar fields from neighboring magnets.

```{code-cell} ipython3
from flatspin.model import SquareSpinIceClosed
model = SquareSpinIceClosed()
animate_switching(model)
```

The switching process of many spin systems is discussed further in [](dynamics).
