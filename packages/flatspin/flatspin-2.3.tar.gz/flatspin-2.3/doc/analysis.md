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

(analysis)=

# Analysis

flatspin provides several tools for analysing simulation results.

+++

(analysis-grid)=
## Working with the grid

Spins in flatspin can be mapped onto a regular grid, which allows for some interesting analysis and useful functionality.
The grid is what enables [spatial vector fields](fields:spatial), for example.

A grid is essentially a bidirectional mapping from spin positions to grid cells.
The flatspin model includes several methods for working with grids.
To create a grid object (the mapping), use {func}`grid() <flatspin.model.SpinIce.grid>`.
By default, a grid is created such that a cell contains at most one spin:

```{code-cell} ipython3
from flatspin.model import SquareSpinIceClosed

model = SquareSpinIceClosed()
model.plot()

def draw_grid(grid):
    edges = grid.edges()
    xmin, ymin, xmax, ymax = grid.extent
    plt.grid(True, c='#999', alpha=1)

    plt.xticks(edges[0])
    plt.yticks(edges[1])
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

grid = model.grid()
draw_grid(grid)
```

The spacing between each grid can be specified with `cell_size`; if `cell_size > lattice_spacing` then a grid call may contain more than one spin:

```{code-cell} ipython3
grid = model.grid(cell_size=(1.5, 1.5))
draw_grid(grid)
model.plot();
```

Alternatively, {func}`fixed_grid() <flatspin.model.SpinIce.fixed_grid>` can be used to create a grid of some fixed size:

```{code-cell} ipython3
grid = model.fixed_grid((4,4))
draw_grid(grid)
model.plot();
```

The {func}`grid() <flatspin.model.SpinIce.grid>` and {func}`fixed_grid() <flatspin.model.SpinIce.fixed_grid>` functions used above return a {class}`Grid <flatspin.grid.Grid>` object.

A {class}`Grid <flatspin.grid.Grid>` can also be created manually, given a collection of points:

```{code-cell} ipython3
from flatspin.grid import Grid

x = np.arange(11)
y = np.abs(x-5)
points = np.column_stack([x, y])

# When called without a cell_size, Grid attempts to auto-detect a
# suitable cell_size such that each cell contains at most one point.
grid = Grid(points)
# For a fixed grid, use Grid.fixed_grid(points, grid_size)

plt.scatter(x, y)
draw_grid(grid)
```

### Looking up spins on the grid
The {class}`Grid <flatspin.grid.Grid>` object enables fast lookup of the grid cell containing any spin.
To map spin indices to grid cells, use {func}`grid_index() <flatspin.grid.Grid.grid_index>`.
To get a list of spins inside a grid cell, use {func}`point_index() <flatspin.grid.Grid.point_index>`.

```{code-cell} ipython3
grid = model.grid(cell_size=(1.5, 1.5))

print('Spin 5 in cell:', grid.grid_index(5))
print('Spin 28 in cell:', grid.grid_index(28))
print('Cell (0,0) contains:', grid.point_index((0,0)))
print('Cell (2,1) contains:', grid.point_index((2,1)))

model.plot()
# Label spin indices for reference
for i in model.indices():
    plt.text(model.pos[i,0], model.pos[i,1], str(i), ha='center', va='center')
draw_grid(grid)
```

### Mapping grid values to spins
A common use case is to create a grid with values, and map each value onto some property of the spins:

```{code-cell} ipython3
# 2D array representing grid with values
# Note that the origin of the grid is in the bottom-left, hence
# the first row of values map to the bottom row of the grid
values = np.array(
    [[-1, -1, 1],
     [-1, 1, -1],
     [-1, 1, 1]])
# Create an appropriate fixed grid
grid = model.fixed_grid((values.shape[1], values.shape[0]))

# Map all spin indices to grid index
spin_inds = model.all_indices()
grid_inds = grid.grid_index(spin_inds)

# Set spin based on grid values
model.spin[spin_inds] = values[grid_inds]

draw_grid(grid)
model.plot();
```

The model provides a convenient shorthand for the above code called {func}`set_grid() <flatspin.model.SpinIce.set_grid>`.
For example, we could spatially arrange the switching thresholds:

```{code-cell} ipython3
values = np.array([
    [0.1, 0.2, 0.3],
    [0.2, 0.3, 0.4],
    [0.3, 0.4, 0.5]
])

model.set_grid('threshold', values)

draw_grid(grid)
quiv = model.plot(C=model.threshold, cmap='coolwarm')
plt.colorbar(quiv, label='threshold');
```

### Mapping spin values to the grid

Going the other way around, we may wish to aggregate some spin value onto each grid cell.

```{code-cell} ipython3
# Count number of spins in each grid cell
grid.add_values(np.ones(model.spin_count))
```

```{code-cell} ipython3
# Sum the spins in each grid cell
grid.add_values(model.spin)
```

```{code-cell} ipython3
# Mean spin in each cell
grid.add_values(model.spin, method='mean')
```

```{code-cell} ipython3
# Plot total magnetization in each cell
from flatspin.plotting import plot_vectors

plt.subplot(121)
UV = grid.add_values(model.vectors, method='sum')
x, y = grid.centers()
XY = np.column_stack([x, y])
plot_vectors(XY, UV, normalize=True);

plt.subplot(122)
model.plot()
draw_grid(grid)
plt.tight_layout();
```

(analysis-vertices)=
## Vertices

Spin ice systems are frequently analyzed in terms of its *vertices*.
A *vertex* is defined by the points in the geometry where spins point either in or out.
In square spin ice, a vertex is surrounded by four spins.
In the plot below, the colored dots denote the vertices.

```{code-cell} ipython3
model.randomize(seed=0x9876)
model.plot()
model.plot_vertices();
```

The spin indices of each vertex can be obtained with {func}`vertices() <flatspin.model.SpinIce.vertices>`:

```{code-cell} ipython3
model.vertices()
```

Given a vertex (list of spin indices), we can obtain its position:

```{code-cell} ipython3
v = [5, 9, 10, 14]
model.vertex_pos(v)
```

... or its magnetization:

```{code-cell} ipython3
model.vertex_mag(v)
```

### Vertex types
The *vertex type* is defined by the dipolar energy between the spins in the vertex.
In the plot above, the colors of the dots indicate the vertex type: green for type 1 (lowest energy), blue for type 2, red for type 3 and gray for type 4 (highest energy).

Use {func}`vertex_type() <flatspin.model.SpinIce.vertex_type>` to get the type of a vertex:

```{code-cell} ipython3
[model.vertex_type(v) for v in model.vertices()]
```

A measure of the degree of frustration in a spin ice system is the *vertex count*:

```{code-cell} ipython3
print("Vertex counts:", model.vertex_count())
```

... or as fractions of the number of vertices, the *vertex population*:

```{code-cell} ipython3
print("Vertex population:", model.vertex_population())
```

### Vertex magnetization

+++

We may also be interested in the *vertex magnetization*:

```{code-cell} ipython3
model.plot_vertex_mag();
```

(analysis-vertex-detection)=
### Vertex detection

Vertices are detected automatically using the {mod}`flatspin.vertices` module.
You can use the module to find vertices of a geometry given a list of spin positions and angles, i.e., without having to create a [model object](model).
Vertex detection relies on the [Grid](analysis-grid) to find vertex locations, using a sliding window of some size.

```{code-cell} ipython3
from flatspin.model import KagomeSpinIce

# Pretend we have no model object
model2 = KagomeSpinIce(size=(3,3), init='random')
pos = model2.pos
angle = model2.angle
spin = model2.spin
mag = model2.vectors
grid = Grid(pos)

plot_vectors(pos, mag)
# Label spin indices for reference
for i in range(len(pos)):
    plt.text(pos[i,0], pos[i,1], str(i), ha='center', va='center')
draw_grid(grid)
```

For kagome spin ice, vertices fall inside a 3x2 grid window:

```{code-cell} ipython3
from flatspin.vertices import find_vertices, vertex_pos, vertex_type

win_size = (2, 3)
vi, vj, vertices = find_vertices(grid, pos, angle, win_size)
display(vertices)
```

```{code-cell} ipython3
vpos = vertex_pos(pos, vertices)
vtype = [vertex_type(spin[v], pos[v], angle[v]) for v in vertices]
print(vtype)

plot_vectors(pos, mag)
plt.scatter(*vpos.T, c=vtype, cmap='vertex-type');
```

(analysis-energy)=
## Energy

The energy of each spin is derived from the total fields acting on each spin, i.e., the dipolar fields, external fields and thermal fields:

$E_i = \vec{h}_i \cdot m_i$

In other words, the energy of spin $i$ is the total field acting on the spin, projected onto its magnetization vector.
Hence only the parallel component of the field contributes to the energy.

Below we obtain the energy of each spin by calling {func}`energy() <flatspin.model.SpinIce.energy>`.
Next we use the energy to color the arrows of each spin in a relaxed pinwheel system.
Notice how the spins that are part of the domain walls (the boundaries of the ferromagnetic domains) have higher energy than the spins that are well inside the domains.

```{note}
The unit of the energy is solely the Zeeman energy, derived from the field at each spin multiplied by its magnetization.
Because flatspin uses reduced magnetization units, i.e., for each spin $m_i = 1$, the energy provided by {func}`energy() <flatspin.model.SpinIce.energy>` also follows this reduced unit scheme (only implicitly multiplied by $m_i = 1$).
To retrieve a physical energy unit, simply multiply the value by the field unit and whatever magnetization you want to ascribe to a single spin.
```

```{code-cell} ipython3
from flatspin.model import PinwheelSpinIceLuckyKnot
model = PinwheelSpinIceLuckyKnot(size=(25,25), alpha=0.1, init='random', use_opencl=True)

print("Total energy (randomized):", model.total_energy())

model.relax()
#model.plot_vertex_mag();
#plt.figure()

E = model.energy()
print("Total energy (relaxed):", np.sum(E))

quiv = model.plot(C=E, cmap='plasma')
plt.colorbar(quiv);
```

Since {func}`energy() <flatspin.model.SpinIce.energy>` considers all fields in the energy calculations, an external field will change the energy landscape:

```{code-cell} ipython3
# Saturating field
model.set_h_ext([0.2, 0.2])

E = model.energy()
print("Total energy (with h_ext):", np.sum(E))

quiv = model.plot(C=E, cmap='plasma')
plt.colorbar(quiv);
```

In the above plot, notice how the domain with the highest energy is pointing antiparallel to the external field.

+++

### Dipolar energy

If we consider dipolar fields only, we obtain the dipolar energy:

$E_\text{dip} = \vec{h}_\text{dip}^{(i)} \cdot m_i$

The dipolar energy is a measure of frustration in the system, and can be obtained with {func}`dipolar_energy() <flatspin.model.SpinIce.dipolar_energy>`:

```{code-cell} ipython3
E_dip = model.dipolar_energy()
print("Total dipolar energy:", np.sum(E_dip))

plt.figure()
plt.title(f"E_dip = {np.sum(E_dip):g}")
quiv = model.plot(C=E_dip, cmap='plasma')
plt.colorbar(quiv);

# Apply saturating field
model.set_h_ext([0.2, 0.2])
model.relax()

E_dip = model.dipolar_energy()
print("Total dipolar energy (after saturation):", np.sum(E_dip))

plt.figure()
plt.title(f"E_dip = {np.sum(E_dip):g}")
quiv = model.plot(C=E_dip, cmap='plasma')
plt.colorbar(quiv);
```

Similarly, there is {func}`external_energy() <flatspin.model.SpinIce.external_energy>` to calculate energy from external fields only, and {func}`thermal_energy() <flatspin.model.SpinIce.thermal_energy>` to calculate energy from thermal fields.
