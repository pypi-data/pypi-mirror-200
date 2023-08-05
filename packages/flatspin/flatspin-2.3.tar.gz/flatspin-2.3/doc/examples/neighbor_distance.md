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
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
plt.rcParams['animation.frame_format'] = "svg"
```

# Neighbor distance

The dipole field felt by each spin is calculated by summing the dipole field contributions from spins in its neighborhood.
The `neighbor_distance` parameter sets the size of the neighborhood to consider when calculating dipole interactions.
Specifically, all spins within a distance of `lattice_spacing * neighbor_distance` are considered neighbors of a spin.
Although it is possible to use `neighbor_distance=np.inf` for a global neighborhood, this is computationally expensive and (usually) unnecessary, because spins far away have neglible contributions to the total dipole field.

The required `neighbor_distance` depends on the system under study, i.e., the specific geometry. 
Care must be taken to include enough spins in the neighborhood such that the observed behavior converges, especially when considering systems exhibiting long-range effects.

In this example, we compare the effect of `neighbor_distance` on two different systems:
* Square spin ice, where local interactions are dominating
* Pinwheel spin ice, where long-range interactions are significant

Here we set the dipolar coupling parameter `alpha` artificially high to relax each system into a low energy state.
Then we investigate how the resulting spin states and vertex populations change as we vary `neighbor_distance`.

```{code-cell} ipython3
params = {
    'size': (25,25),
    'init': 'random',
    'random_seed': 42,
    'alpha': 1.0,
    'use_opencl': 1,
    'disorder': 0.04,
}
```

```{code-cell} ipython3
from flatspin.model import SquareSpinIceClosed, PinwheelSpinIceDiamond
from flatspin.plotting import montage_fig

# Preview the two geometries
square = SquareSpinIceClosed(**params)
pinwheel = PinwheelSpinIceDiamond(**params)

plt.figure(figsize=(6, 4))
plt.subplot(121)
plt.axis('off')
plt.title("Square")
square.plot()

plt.subplot(122)
plt.axis('off')
plt.title("Pinwheel")
pinwheel.plot()

plt.tight_layout();
```

## Relaxation with high alpha

Below we plot the vertex magnetization of the initial random state, and after calling `relax()`.

```{code-cell} ipython3
plt.figure(figsize=(6, 6))

plt.subplot(221)
plt.axis('off')
plt.title("Square: init")
square.plot_vertex_mag()

plt.subplot(222)
plt.axis('off')
plt.title("Pinwheel: init")
pinwheel.plot_vertex_mag()

square.relax()
plt.subplot(223)
plt.axis('off')
plt.title("Square: relaxed")
square.plot_vertex_mag()

pinwheel.relax()
plt.subplot(224)
plt.axis('off')
plt.title("Pinwheel: relaxed")
pinwheel.plot_vertex_mag()

plt.tight_layout();
```

## Effect of `neighbor_distance`

The function below performs the above relaxation for a range of `neighbor_distance`, and records the resulting spin state and vertex population.
Note that the initial state of the system is the same, since we use the same `random_seed`.

```{code-cell} ipython3
def run_neighbor_distance(model_class, max_neighbor_dist=20, **params):
    # Run relax() for different values of neighbor_distance
    spins = []
    vpops = []
    neighbor_dists = np.arange(1, max_neighbor_dist+1)

    for nd in neighbor_dists:
        # neighbor_distance must be set at model initialization time
        si = model_class(neighbor_distance=nd, **params)
        si.relax()

        spins.append(si.spin.copy())

        types, counts = si.vertex_population()
        vpop = [0, 0, 0, 0]
        for vt, c in zip(types, counts):
            vpop[vt-1] = c
        vpops.append(vpop)

    result = {
        'spins': spins,
        'vertex_populations': vpops,
        'neighbor_dists': neighbor_dists,
    }

    return result
```

Below we define some functions for visualizing the results:
1. Animation of how the relaxed spin states change as `neighbor_distance` is varied
2. Plot vertex population as a function of `neighbor_distance`

```{code-cell} ipython3
def animate_spins(model, spins, neighbor_dists, **kwargs):
    # Animate list of spin states
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0, right=1, bottom=0.0, top=.9, wspace=0, hspace=0)

    def animate(i):
        model.set_spin(spins[i])
        ax.cla()
        ax.set_axis_off()
        ax.set_title(f"neighbor_distance={neighbor_dists[i]}")
        model.plot_vertex_mag(ax=ax)

    anim = FuncAnimation(
        fig, animate, init_func=lambda: None,
        frames=len(spins), interval=500, blit=False
    )
    plt.close() # Only show the animation
    return HTML(anim.to_jshtml())

def plot_vertex_populations(spins, neighbor_dists, vertex_populations, **kwargs):
    # Plot vertex populations as function if neighbor_distance
    vpops = np.array(vertex_populations)
    for t in range(4):
        plt.plot(neighbor_dists, vpops[:,t], label=f"Type {t+1}")
    plt.xlabel("Neighbor distance")
    plt.ylabel("Vertex population")
    plt.legend();
```

## Results: square spin ice

```{code-cell} ipython3
result_square = run_neighbor_distance(SquareSpinIceClosed, max_neighbor_dist=30, **params)
```

In the animation below, we see visually how the relaxed spin state changes as we vary `neighbor_distance`.
Observe how the state does indeed change over a significant range of `neighbor_distance`.
However, qualitatively the states are fairly similar, e.g., compare the size of the emergent antiferromagnetic domains (white regions).

```{code-cell} ipython3
animate_spins(square, **result_square)
```

Although the final state of the system is clearly sensitive to `neighbor_distance`, the plot below shows how the statistical measure of vertex populations change over `neighbor_distance`.
As can be seen, the vertex populations do not vary significantly beyond `neighbor_distance=4`.
This is because square spin ice is dominated by local interactions.

```{code-cell} ipython3
plot_vertex_populations(**result_square)
```

## Results: pinwheel spin ice

```{code-cell} ipython3
result_pinwheel = run_neighbor_distance(PinwheelSpinIceDiamond, max_neighbor_dist=30, **params)
```

The animation below shows the final state of pinwheel spin ice for different values `neighbor_distance`.
Again, the final state is indeed different across a significant range of `neighbor_distance`.
However, there seems to be more differences up until approximately `neighbor_distance=10`, after which the states are more qualitatively similar.

```{code-cell} ipython3
animate_spins(pinwheel, **result_pinwheel)
```

Again, plotting the vertex populations for pinwheel spin ice, we see that they do not change significantly beyond `neighbor_distance=10`.
Because pinwheel spin ice exhibits significant long-range interactions, a larger `neighbor_distance` is needed for convergence, compared to square spin ice.

```{code-cell} ipython3
plot_vertex_populations(**result_pinwheel)
```
