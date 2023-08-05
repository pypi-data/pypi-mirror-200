---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
:tags: [remove-input]

%config InlineBackend.figure_formats = ['svg']

import numpy as np
from numpy.linalg import norm
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
plt.rcParams['animation.frame_format'] = "svg"
```

(anneal-field)=
# Field based annealing

This example shows how to set up a field-based annealing protocol.
Below we anneal square spin ice using a rotating field, whose strength is gradually decreased.
Disorder introduces small variations in the coercive fields, which actually helps the annealing process by creating nucleation points in the lattice.

```{code-cell} ipython3
from flatspin.model import SquareSpinIceClosed

model = SquareSpinIceClosed(size=(25,25), disorder=0.05, use_opencl=True)
model.plot_vertex_mag();
```

## Rotating field protocol

+++

We use the {class}`Rotate <flatspin.encoder.Rotate>` encoder to set up the external rotating field.
The `timesteps` parameter denotes the resolution of one full rotation, while `H0` and `H` sets the minimum and maximum field strength, respectively. The length of the `input` array defines the number of rotations (20), while the values define the field strength for each rotation, where a value of `1.0` is mapped to `H`, and a value of `0.0` maps to `H0`.

```{code-cell} ipython3
from flatspin.encoder import Rotate

timesteps = 64
enc = Rotate(H=0.09, H0=0.06, timesteps=timesteps)
input = np.linspace(1, 0, 20)

h_ext = enc(input)
H = norm(h_ext, axis=1)

plt.plot(norm(h_ext, axis=1), label="norm(h_ext)")
plt.plot(h_ext[:,0], label="h_ext[0]")
plt.plot(h_ext[:,1], label="h_ext[1]")
plt.xlabel("time step")
plt.ylabel("h_ext [T]")
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0));
```

## Run the field protocol

Below we iterate over each `h_ext` value in the field protocol, and update the model accordingly. We record the number of spin flips (`steps`) and dipolar energy (`E_dip`) per field value. At the end of each rotation, we also take a snapshot of the `spin` array.

```{code-cell} ipython3
# Start in polarized state
model.polarize()

# Record spins, number of spin flips and dipolar energy over time
spins = []
flips = []
E_dip = []
for i, h in enumerate(h_ext):
    model.set_h_ext(h)
    s = model.relax()
    if (i+1) % timesteps == 0:
        # Record spin state at the end of each rotation
        spins.append(model.spin.copy())
    flips.append(s)
    E_dip.append(model.total_dipolar_energy())

print(f"Completed {sum(flips)} steps")
```

## Spin flips over time

Here we plot the total number of spin flips per field strength, i.e., per field rotation. As can be seen, the strongest fields saturates the array by flipping every spin twice. As the field strength decreases, so does the number of spin flips. Eventually the field becomes too weak to flip any spins.

```{code-cell} ipython3
H = norm(h_ext, axis=-1).round(10)
df = pd.DataFrame({'H': H, 'flips': flips})
df.groupby('H', sort=False).sum().plot(legend=False)
plt.gca().invert_xaxis()
plt.ylabel("Spin flips")
plt.xlabel("Field strength [T]");
```

## Dipolar energy

The total dipolar energy is the sum of the dipolar fields acting anti-parallel to the spin magnetization. It is a measure of the total frustration in the system, and a good measure of how well the system has annealed.

```{code-cell} ipython3
plt.plot(E_dip)
```

## Animation of the annealing process

Finally we animate the annealing process by plotting vertex magnetization at the end of each rotation.
In the animation below we see the emergence of antiferromagnetic domains (white regions), which correspond to low energy states. The domains are separated by domain walls with a net positive magnetic moment.

```{code-cell} ipython3
fig, ax = plt.subplots()

def animate_spin(i):
    H = norm(h_ext[(i+1) * timesteps - 1])
    ax.set_title(f"H={H:.3f} [T]")
    model.set_spin(spins[i])
    model.plot_vertex_mag(ax=ax, replace=True)
        
anim = FuncAnimation(fig, animate_spin, frames=len(spins), interval=200, blit=False)
plt.close() # Only show the animation
HTML(anim.to_jshtml())
```
