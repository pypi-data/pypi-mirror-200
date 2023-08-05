---
jupytext:
  formats: ipynb,md:myst
  text_representation: {extension: .md, format_name: myst, format_version: 0.13, jupytext_version: 1.11.5}
kernelspec: {display_name: Python 3, language: python, name: python3}
---

```{code-cell} ipython3
:tags: [remove-input]

import numpy as np
from numpy.linalg import norm
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.rcParams['animation.frame_format'] = "svg"
%config InlineBackend.figure_formats = ['svg']
```

## Square ASI robustness to dilution defects

In this example we generate geometries of dilute square ASI and relax them by a rotating, global field.
The results analyzed in terms of vertex type population and their robustness to increasing dilution fraction.

We first create the dilute ensembles from a square ASI.
The ensembles are relaxed with a rotating field protocol in flatspin.
Finally, we analyze the results with respect to vertex type populations.

+++

### Creating dilute ensembles
First, we generate the example system: a complete square ASI.
We will then iteratively remove magnets and save the resulting systems.

```{code-cell} ipython3
from flatspin.model import SquareSpinIceClosed, CustomSpinIce
from flatspin.plotting import plot_vector_image

size = (50, 50)
sq_asi = SquareSpinIceClosed(size = size, lattice_spacing = 1)

plt.figure(figsize=(10,6))
plt.title(f'Full original ensemble, size = {size}')
sq_asi.plot();
```

Next, we define the dilution fractions and the corresponding number of magnets to be removed at each dilution fraction.

```{code-cell} ipython3
asi_size_n = sq_asi.spin_count

dilutions = np.array([0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4])
num_removed = [round(d*asi_size_n) for d in dilutions]

print(f"For {asi_size_n} total magnets")
df = pd.DataFrame({'dilution fraction': dilutions, 'magnets removed': num_removed })
display(df)
```

We now define the dilute geometries, using several random seeds for the stochastic removal of magnets.
The geometries are saved as files where the positions and angles of each spin are stored, to be used by the {class}`CustomSpinIce <flatspin.model.CustomSpinIce>` model class.

```{code-cell} ipython3
root_dir = 'dilution'
if not os.path.exists(root_dir):
    os.makedirs(root_dir)
    print(f"Creating directory {root_dir}")

square_geom = (sq_asi.pos, sq_asi.angle)

random_iterations = 10
for rand_seed in range(random_iterations):
    # Order the ids of the magnets. The order in which they are removed
    np.random.seed(rand_seed)
    removed_id = np.random.choice(asi_size_n, size=max(num_removed), replace=False)

    for i, n in enumerate(num_removed):
        square_geom_removed = (np.delete(square_geom[0], removed_id[:n], axis = 0),
                           np.delete(square_geom[1], removed_id[:n], axis = 0))
        # Save coordinates and angles
        np.savetxt(f'{root_dir}/coords-dilution-{str(i).zfill(2)}-seed-{str(rand_seed).zfill(2)}.csv', (square_geom_removed[0]))
        np.savetxt(f'{root_dir}/angles-dilution-{str(i).zfill(2)}-seed-{str(rand_seed).zfill(2)}.csv', (square_geom_removed[1]))
```

We can instantiate a CustomSpinIce example model from one of these generated geometries:

```{code-cell} ipython3
dilute_example = CustomSpinIce(magnet_coords = f'{root_dir}/coords-dilution-06-seed-00.csv',
                               magnet_angles = f'{root_dir}/angles-dilution-06-seed-00.csv',
                               radians = True)

plt.figure(figsize=(10,6))
plt.title(f'Dilute ensemble, size = {size}, dilution = {1-dilute_example.spin_count/asi_size_n:.2f}')
dilute_example.plot();
```

### Baseline field annealing

We test a field annealing approach for the undiluted system here, before we generate the runs for all diluted systems. See the [field annealing documentation](anneal-field) for an example of how to set this up.

First, we define some physical parameters of the simulation and a model instance:

```{code-cell} ipython3
# Size of magnets
w, l, t = 220e-9, 80e-9, 20e-9 # [m]
volume = w*l*t # [m^3]
M_sat = 860e3 # [A/m]
M_i = M_sat * volume

a = 1e-9 # lattice_spacing unit [m]
lattice_spacing = 300 # [a]

mu_0 = 1.25663706e-6 # m kg /s^2 A^2
alpha = mu_0 * M_i / (4 * np.pi * a**3)

# Astroid parameters
sw_b = 0.38
sw_c = 1
sw_beta = 1.3
sw_gamma = 3.6


rand_seed = 0
disorder = 0.05
neighbor_distance = 3

test_size = (10,10)

model = SquareSpinIceClosed(size=test_size, lattice_spacing=lattice_spacing, alpha=alpha,
                            disorder=disorder, neighbor_distance=neighbor_distance,
                            sw_b=sw_b, sw_c=sw_c, sw_beta=sw_beta, sw_gamma=sw_gamma,
                            random_seed=rand_seed, use_opencl=1)
```

Next, we use the `Rotate` encoder and find some fitting field values that will relax the system with a rotating field.
We can adjust the parameter values to see the effect.
The current parameters are the ones used for the experiment in the paper, which takes a while to run, even for the smaller test system.

```{code-cell} ipython3
from flatspin.encoder import Rotate

# We define the decreasing field strength
H_hi, H_low = 0.080, 0.072
input_values = np.arange(1,0,-0.001)
timesteps = 100 # (per input value)

# Define the external field values based on the Rotate encoder
encoder = Rotate(H = H_hi, H0 = H_low, timesteps=timesteps)
h_ext = encoder(input_values)

# Start in polarized state
model.polarize()

# Record spins and number of spin flips over time
spins = []
flips = []
for i, h in enumerate(h_ext):
    model.set_h_ext(h)
    s = model.relax()
    # Record spin state at the end of each rotation
    if (i+1) % timesteps == 0:
        spins.append(model.spin.copy())
    flips.append(s)

print(f"Completed {sum(flips)} flips")
```

```{code-cell} ipython3
H = norm(h_ext, axis=-1).round(10)
df = pd.DataFrame({'H': H, 'flips': flips})
df.groupby('H', sort=False).sum().plot(figsize=(10,6))
plt.gca().invert_xaxis()
plt.ylabel("Spin flips")
plt.xlabel("Field strength [T]");
```

For a too strong (saturating) field strength, all the magnets will be flipped by the field.
The maximum number of flips in one rotation of the field, i.e., at one field strength, is twice the total number of magnets (1 flip + 1 flip back).
The number of timesteps and the field strength parameters should be tuned so that we start out flipping almost all the magnets (i.e., a strong *enough* field to change the system state) and go until we don't flip any magnets as we don't need to simulate weaker fields than that which results in no activity.


Below, we animate over the states of the relaxation process (skipping quite a few frames).

```{code-cell} ipython3
:tags: [hide-input]

from matplotlib.animation import FuncAnimation
from IPython.display import HTML

fig, ax = plt.subplots()

skip_frames = 20
def animate_spin(i):
    i = i*skip_frames
    H = norm(h_ext[(i+1) * timesteps - 1])
    ax.set_title(f"H={H:.3f} [T]")
    model.set_spin(spins[i])
    model.plot_vertex_mag(ax=ax, replace=True)

anim = FuncAnimation(fig, animate_spin, frames=len(spins[::skip_frames]), interval=200, blit=False)
plt.close() # Only show the animation
HTML(anim.to_jshtml())
```

### Create the runs to generate the data.

We can now generate the data for all the dilute systems and different random seeds.
We generate a command that can schedule a whole sweep of jobs based on the generated dilute geometries.

```{code-cell} ipython3
# Generate flatspin-run-sweep command
print("\nGENERATED COMMAND: \n")
print(f"flatspin-run-sweep -r dist -m CustomSpinIce -e Rotate ", end='\n')
print(f"-p sw_b={sw_b} -p sw_c={sw_c} -p sw_beta={sw_beta} -p sw_gamma={sw_gamma} ", end='\n')
print(f"-p alpha={alpha:.2f} -p lattice_spacing={lattice_spacing} -p disorder={disorder} ", end='\n')
print(f"-p neighbor_distance={neighbor_distance} ", end='\n')
print(f"-p 'input=np.arange(1,0,-0.001)' ", end='\n')
print(f"-p timesteps={timesteps} -p H={H_hi} -p H0={H_low} ", end='\n')
print(f"-s 'num=range(10)' -s 'rs=range(10)' ", end='\n')
print(f"-s 'magnet_coords=[\"coords-dilution-\"+str(num).zfill(2)+\"-seed-\"+str(rs).zfill(2)+\".csv\"]' ", end='\n')
print(f"-s 'magnet_angles=[\"angles-dilution-\"+str(num).zfill(2)+\"-seed-\"+str(rs).zfill(2)+\".csv\"]' ", end='\n')

print("-o CHANGE_TO_OUTPUT_FOLDER")
```

### Analyze generated data

The dataset can also be {download}`downloaded here </data/flatspin/dilution-example-run.zip>`.

```{code-cell} ipython3
from flatspin.data import Dataset, read_table, read_geometry, vector_grid
from flatspin.grid import Grid
from flatspin.vertices import find_vertices, vertex_type

data_path = '/data/flatspin/dilution-example-run'

D = Dataset.read(data_path)
display(D.index)
```

We now count all the vertices and their types for all the different runs.
This might take some time.

```{code-cell} ipython3
from collections import defaultdict
from joblib import Parallel, delayed

def count_types(ds):
    dilution_num = int(ds.index['num'])
    rand_seed = int(ds.index['rs'])
    spins = read_table(ds.tablefile('spin'), index_col='t')
    
    # Choose the final spin state at t=-1
    spins_final = spins.iloc[-1]

    geom = read_geometry(ds.tablefile('geometry'))
    pos, angles = geom
    grid = Grid(pos)

    # Identify vertices (only complete vertices)
    _, _, vertices = find_vertices(grid, pos, angles, 3)

    # Sort vertices by type
    types = [vertex_type([spins_final[s] for s in v],
                         [pos[s] for s in v],
                         [angles[s] for s in v])
             for v in vertices]

    # Count the vertex types
    vertex_types, counts = np.unique(types, return_counts=True)
    typecount = dict(zip(vertex_types, counts))
    
    return dilution_num, rand_seed, counts

queue = D[0::10]
types_by_dilution = Parallel(n_jobs=10, verbose=0)(delayed(count_types)(ds) for ds in queue)

df_types = pd.DataFrame(types_by_dilution, columns={'dilution': 'num', 'rand_seed': 'rs', 'type': 'type'})
label_types = ['Type I', 'Type II', 'Type III', 'Type IV']

df_types[label_types[:-1]] = pd.DataFrame(df_types.type.tolist(), index= df_types.index)
df_types_avg = df_types.groupby('dilution').mean()
sum_magnets = df_types_avg[label_types[:-1]].sum(axis=1)
df_types_avg[[l+'_frac' for l in label_types[:-1]]] = (df_types_avg[label_types[:-1]].T/sum_magnets).T
df_types_avg
```

### Plotting the results

First, let's look at each dilution fraction for one selected random seed.

```{code-cell} ipython3
:tags: [hide-input]

def read_data_vertices_grid(dataset, t=[0]):
    ''' Return the positions and magnetization of the dataset's vertices '''
    grid_size = None
    crop_width = ((1,1),(1,1))
    win_shape, win_step = ((3,3), (2, 2))

    df = read_table(dataset.tablefile('mag'), index_col='t')
    UV = np.array(df)
    UV = UV.reshape((UV.shape[0], -1, 2))
    UV = UV[t]

    pos, angle = read_geometry(dataset.tablefile('geometry'))

    XY, UV = vector_grid(pos, UV, grid_size, crop_width, win_shape, win_step, normalize=False)
    return XY, UV/2

def plot_vertices(XY, UVi, ax):
    ax.axis('off')
    plot_vector_image(XY, UVi, ax=ax, replace=True)
```

```{code-cell} ipython3
# Load final states (might take some time)
final_dilution_states = dict()
for num, ds in D[D.index['rs']==0].groupby('num'):
    final_dilution_states[dilutions[num]] = read_data_vertices_grid(ds, t=-1)
```

```{code-cell} ipython3
# Plot final states
fig, axs = plt.subplots(2, 5, figsize=(10,4), dpi=100)
for ax, (dilution, vstate) in zip(axs.flat, final_dilution_states.items()):
    ax.set_title(f'dilution = {dilution}')
    XY, UVi = vstate
    mag = np.amax(np.linalg.norm(UVi, axis=-1))
    plot_vertices(XY, UVi/mag, ax)
fig.suptitle('Final timestep', fontsize='x-large');
```

Finally, we plot the vertex type as a function of dilution fraction.

```{code-cell} ipython3
df_types_avg['Type IV_frac'] = 0.0

plt.figure(figsize=(10,6))
for label, ts in zip(label_types, df_types_avg[[l+'_frac' for l in label_types]]):
    plt.plot(dilutions[:-1], df_types_avg[ts], marker = 'x', label=label)
    plt.xscale('log')
plt.ylabel('Average vertex fraction')
plt.xlabel('Dilution fraction')
plt.legend();
```
