---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
:tags: [remove-input]

import numpy as np
import matplotlib.pyplot as plt
```

# Dirac Strings in Kagome ASI
Here we demonstrate how flatspin was to produce Dirac Strings following the experimental setup given by {cite}`mengotti2011`.

[“Real-space observation of emergent magnetic monopoles and associated Dirac strings in artificial kagome spin ice” Nature Phys 7, 68–74 (2011)](https://doi.org/10.1038/nphys1794)

The flatspin results are discussed in more detail in our paper {cite}`Flatspin2022`.

+++

## Creating the Dataset
We set our parameters to closely match the experimental setup in {cite}`mengotti2011`.

Below is the `flatspin-run` command used to generate the dataset for this section, followed by an explaination of the parameters used.

```flatspin-run -m KagomeSpinIceRotated -e Triangle -p phase=0 -p phi=-3.6 -p "size=(29,29)" -p temperature=300 -p H=0.1 -p periods=1  -p sw_beta=2.5 -p sw_b=0.212 -p sw_gamma=3 -p sw_c=1 -p hc=0.216 -p alpha=0.00103 -p use_opencl=1 -p neighbor_distance=10 -p disorder=0.05  -p "m_therm=0.05*1.29344e-15" -p timesteps=2000 -p spp=2000 -o diracStringsPublish2```

`-m KagomeSpinIceRotated` and `-p size=(29,29)` define the geometry and the number of magnets similar to the experimental setup.

`-e Triangle`, `-p phi=-3.6` and `-p phase=0` uses a Triangle encoder to set up a reversal field at an angle of -3.6 degrees.  As `H=0.1`, the field starts at -0.1 T ramps up linearly to 0.1 T then back down to -0.1 T

A `temperature` of 300 K is used to simulate room temperature.

Using a magnetization saturation ($M_S$) of 860 kA/m, and the volume of the magnets given in the experimental setup (~1.5e-21 m^3), the `m_therm` parameter is taken to be 5% of volume * msat.

The value of `alpha` is calculated from $\alpha = \frac{\mu_0 M}{4\pi a^3}$ (see [](theory)), with $M$ = 860e3 * 1.504e-21 Am^2 and $a$ = 500 nm

Micromagnetic simulations of magnets with this msat and the given dimensions (470 nm * 160 nm * 20 nm) were used to obtain the switching parameters `sw_beta=2.5`, `sw_b=0.212`, `sw_gamma=3`, `sw_c=1` and `hc=0.216`.

5% disorder was used to account for variations in the magnets used in the experiments.

+++

## Calculate $H_c$
First we analyze the dataset created by the above `flatspin-run` command to calculate the switching field of the full lattice, $H_c$.

```{code-cell} ipython3
from flatspin import data

ds = data.Dataset.read("/data/flatspin/diracStringsPublish2")

# for now we're only interested in the fist half of the run
t = slice(None, 1000)

# using grid_size=(1,1) returns the average magnetization over the whole lattice
mag = data.load_output(ds, "mag", grid_size=(1, 1), t=t)

# get timestep where array switches (the time where the absolute magnetization in the x-direction is minimized)
t_min = np.argmin(abs(mag[:, 0]))
print(f"Timestep where array switches, t_min = {t_min}")

# load the data for the external field and use t_min to get find HC
h_ext = data.load_output(ds, "h_ext", t=t)
Hc = h_ext[t_min][0]
print(f"H_c = {Hc}")
```

## Find the field values of interest
In {cite}`mengotti2011` they show the state of ASI at field values: `[0.8HC, 0.85HC, 0.92HC, 0.95HC, 0.99HC, 1.06HC]`.
To allow us to compare the results of flatspin to the experimental setup, we will find the timesteps in our dataset where the field is closest to these values.

```{code-cell} ipython3
# calculate the fields of interest in terms of our HC
foi = [0.8, 0.85, 0.92, 0.99, 1.06]
foiHC = Hc * np.array(foi)
print(f"foiHC = {foiHC}")

# find the nearest times by minimizing the absolute difference between the field and the HC
nearest_time = [np.argmin(np.abs(field - h_ext[:, 0])) for field in foiHC]
print(f"nearest_time = {nearest_time}")
print(f"nearest fields = {[str(round(h_ext[t, 0]/Hc,2))+'HC' for t in nearest_time]}")
```

Below we animate the state of the ASI, as it evolves from the first to the last field value of interest (`0.8HC` to `1.06HC`).

```{code-cell} ipython3
from IPython.display import HTML
from matplotlib.animation import FuncAnimation
from flatspin.plotting import plot_vectors

def animate_dirac_strings(ds, times):
    fig, ax = plt.subplots(figsize=(7.2, 7.2), facecolor=(0.4, 0.4, 0.4))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=0.95, wspace=0, hspace=0)
    ax.set_axis_off()

    _, UV = data.read_vectors(ds.tablefiles(), "mag", times)
    positions, _ = data.read_geometry(ds.tablefile('geometry'))

    def animate(i):
        plot_vectors(positions, UV[i], replace=True, ax=ax, cmap="peem180")
        ax.set_title(f"{round(h_ext[times[i],0]/Hc,2)}$H_c$", fontsize=20, color="white")


    anim = FuncAnimation(
        fig, animate, init_func=lambda: None,
        frames=len(times), interval=100, blit=False
    )
    plt.close() # Only show the animation
    return HTML(anim.to_jshtml(fps=8))
#animate_dirac_strings(ds, times=nearest_time)
#animate_dirac_strings(ds, times=list(range(710,750,1)))
animate_dirac_strings(ds, times=list(range(nearest_time[0], nearest_time[-1]+1)))
```

## Hysteresis
Now we plot the hysterisis of our dataset, as well as a sketch of the hysteresis shown in {cite}`mengotti2011`.

```{code-cell} ipython3
mag = data.load_output(ds, "mag", grid_size=(1, 1))  # now we want full run length
h_ext = data.load_output(ds, "h_ext")
plt.figure(figsize=(8, 5))
plt.plot(h_ext[:, 0] / Hc, mag[:, 0], label="flatspin")

meng = np.loadtxt("scaledMeng.txt").round(2)  # our rough estimate of the Mengotti et al. dataset inferred from their graph
plt.plot(meng[:, 0], meng[:, 1], label="Mengotti")

#make text marker at the fields of interest
rom_num = ["I", "II", "III", "IV", "V"]
offsetx = [-.1,0,.1,-.3,-.3]
offsety = [-.15,-.15,-.15,0,0]
for i, field in enumerate(foi):
    plt.plot(field, mag[nearest_time[i], 0], ".", label=f"{rom_num[i]}", color="black")
    plt.text(field+offsetx[i], mag[nearest_time[i], 0] + offsety[i], rom_num[i], color="black")
    
plt.xlabel("$H/H_c$")
plt.ylabel("$M/M_S$")
plt.ylim(-1.2, 1.2)
plt.legend(["flatspin", "Mengotti et al."]);
```
