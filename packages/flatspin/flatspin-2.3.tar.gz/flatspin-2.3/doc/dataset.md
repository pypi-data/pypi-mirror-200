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

(dataset)=

# Datasets

It is often useful to save results from flatspin simulations to persistent storage.
Simulations can take a long time, and storing results allows us to perform analysis afterwards without needing to re-run the simulations.
Or maybe we simply wish to archive the results in case we need them later.

Whatever the motiviation, the flatspin dataset provides a powerful format in which to organize and save results.

All the flatspin [command-line tools](cmdline) work with datasets, so a good understanding of the dataset format is essential when working with flatspin data from the command line.

## Anatomy of a dataset

A flatspin dataset consists of three major components:

1. Dictionaries with simulation **parameters** and **information**
2. An **index** of the runs included in the dataset
3. The results of each run, stored in one or more **tables**

As you can see, (1) and (2) is *metadata* about the results, while (3) is the actual result *data*.

## A simple example

Let us begin with a simple example, where we store the results from a single run in a dataset.

First, we run a simulation and store results in two tables: `spin` contains the state of all the spins over time, and `h_ext` contains the external field values.

```{code-cell} ipython3
import pandas as pd
from flatspin.model import PinwheelSpinIceDiamond
from flatspin.encoder import Triangle

# Model parameters
model_params = {
    'size': (4, 4),
    'disorder': 0.05,
    'use_opencl': True,
}

# Encoder parameters
encoder_params = {
    'H': 0.2,
    'phi': 30,
    'phase': 270,
}

# Create the model object
model = PinwheelSpinIceDiamond(**model_params)

# Create the encoder
encoder = Triangle(**encoder_params)

# Use the encoder to create a global external field
input = [1]
h_ext = encoder(input)

# Save spin state over time
spin = []

# Loop over field values and flip spins accordingly
for h in h_ext:
    model.set_h_ext(h)
    model.relax()
    # Take a snapshot (copy) of the spin state
    spin.append(model.spin.copy())

# Create two tables, one for m_tot and one for h_ext
result = {}
result['spin'] = pd.DataFrame(spin)
result['spin'].index.name = 't'
result['h_ext'] = pd.DataFrame(h_ext, columns=['h_extx', 'h_exty'])
result['h_ext'].index.name = 't'

display(result['spin'])
display(result['h_ext'])
```

## Creating the Dataset object

We are now ready to create the {class}`Dataset <flatspin.data.Dataset>` object.
A {class}`Dataset <flatspin.data.Dataset>` object *only contains metadata* about the results, but offers several methods to inspect the results available in the dataset.

```{code-cell} ipython3
import os
import shutil
import flatspin
from flatspin.data import Dataset

# Where to store the dataset and results
basepath = '/tmp/flatspin/mydataset'
if os.path.exists(basepath):
    shutil.rmtree(basepath)

# Create params dictionary
# We store both the model params and encoder params
# (there is no overlap between model and encoder params)
params = model_params.copy()
params.update(encoder.get_params())

# Create info dictionary (misc info)
info = {
    'model': f'{model.__class__.__module__}.{model.__class__.__name__}',
    'version': flatspin.__version__,
    'comment': 'My simple dataset'
}

# Create the index table, with a single entry for the above run
# The index must contain a column named 'outdir' which points
# to the location of the result directory / archive file
outdir = 'myrun.npz'
index = pd.DataFrame({'outdir': [outdir]})

# Create the dataset directory
os.makedirs(basepath)

# Create the dataset object
dataset = Dataset(index, params, info, basepath)
```

Once the dataset object has been created, it can be saved to disk with {func}`Dataset.save() <flatspin.data.Dataset.save>`.

```{code-cell} ipython3
print("Saving dataset:", repr(dataset))
dataset.save()
```

(dataset-saving)=
## Saving results
As mentioned, a {class}`Dataset <flatspin.data.Dataset>` object only keeps track of metadata.
The result tables must be saved separately using {func}`save_table() <flatspin.data.save_table>`, to the location referenced by the `outdir` column in the dataset index.

flatspin tools (and {func}`save_table <flatspin.data.save_table>`) supports a few different table formats, selected based on the file extension:
* `csv`: Simple CSV text files
* `hdf`: A [Hierarchical Data Format](https://pandas.pydata.org/docs/reference/api/pandas.read_hdf.html) archive
* `npy`: [NumPy binary files](https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html)
* `npz`: Compressed archive of .npy files

We recommend using the `npy` or `npz` formats, since they are fast, efficient and easy to work with.

```{note}
Depending on the table format, the `outdir` column in the dataset index refers to either a filesystem directory (in case of `csv` or `npy`) or the name of an archive file (in case of `hdf` or `npz`).
Hence tables are either stored as separate files inside an output directory, or as entries inside an archive file.
```

Below we save the result tables we created earlier in a `npz` archive.

```{code-cell} ipython3
from flatspin.data import save_table

# Save the result tables to the npz archive
for name, df in result.items():
    filename = f"{basepath}/{outdir}/{name}"
    print(f"Saving table {name} to {filename}")
    save_table(df, filename)
```

## The dataset directory

Let us take a look at the files and directories in our newly created dataset:

```{code-cell} ipython3
!tree $dataset.basepath
```

As you can see, the dataset `basepath` directory contains three CSV files: `params.csv` and `info.csv` contain the parameters and misc information (`dataset.params` and `dataset.info`), while `index.csv` contains the index of the runs (`dataset.index`).

`index.csv` contains a list of all the runs included in the dataset.
In this simple example, the dataset contains only one run, with results stored in the archive `myrun.npz`.

```{code-cell} ipython3
!cat $dataset.basepath/index.csv
```

## Reading datasets

To read a dataset from disk, use {func}`Dataset.read() <flatspin.data.Dataset.read>`:

```{code-cell} ipython3
dataset = Dataset.read(basepath)
```

Printing a dataset object produces a summary of its contents:

```{code-cell} ipython3
print(dataset)
```

## Reading results

To read the results from a run, use {func}`tablefile() <flatspin.data.Dataset.tablefile>` to get the path to the table of interest, and {func}`read_table() <flatspin.data.read_table>` to read it into memory:

```{code-cell} ipython3
from flatspin.data import read_table

print(dataset.tablefile('h_ext'))
df = read_table(dataset.tablefile('h_ext'), index_col='t')
display(df)
```

You can also get a list of all available tables with {func}`tablefiles() <flatspin.data.Dataset.tablefiles>`:

```{code-cell} ipython3
dataset.tablefiles()
```

## Datasets with many runs

The real power of the dataset comes apparent when dealing with the results from many simulations.
A common use case is parameter sweeps, where simulations are run repeatedly using different values of some parameter(s).
In this case, we add columns to the index that keep track of the parameters being swept.

In the next example, we sweep the angle `phi` of the external field and store the results from each run in `results`.

```{code-cell} ipython3
# Sweep angle phi of external field
phis = np.arange(0, 41, 10)
results = []
for phi in phis:
    # Model params are not swept in this example
    model = PinwheelSpinIceDiamond(**model_params)
    
    # Override phi from encoder_params
    ep = encoder_params.copy()
    ep['phi'] = phi
    encoder = Triangle(**ep)
    h_ext = encoder([1])
    
    spin = []
    for h in h_ext:
        model.set_h_ext(h)
        model.relax()
        spin.append(model.spin.copy())

    result = {}
    result['spin'] = pd.DataFrame(spin)
    result['spin'].index.name = 't'
    result['h_ext'] = pd.DataFrame(h_ext, columns=['h_extx', 'h_exty'])
    result['h_ext'].index.name = 't'

    results.append(result)

print(len(results), 'results')
```

Next, we create the dataset for the sweep.
The code is the same as earlier, except the `index` now:
* contains several rows of results
* has an additional column `phi` which contains the swept field angles

```{code-cell} ipython3
# Where to store the dataset and results
basepath = '/tmp/flatspin/mysweep'
if os.path.exists(basepath):
    shutil.rmtree(basepath)
os.makedirs(basepath)

# params and info unchanged

# Create the index table, with one entry per value of phi
outdirs = [f'run{i:02d}.npz' for i in range(len(phis))]
index = pd.DataFrame({'phi': phis, 'outdir': outdirs})
display(index)

# Create and save the dataset
dataset = Dataset(index, params, info, basepath)
print("Saving dataset:", repr(dataset))
dataset.save()

# Save the results of each run
for outdir, result in zip(outdirs, results):
    for name, df in result.items():
        filename = f"{basepath}/{outdir}/{name}"
        print(f"Saving table {name} to {filename}")
        save_table(df, filename)
```

When the dataset contains multiple items, {func}`tablefile() <flatspin.data.Dataset.tablefile>` returns a list of files:

```{code-cell} ipython3
dataset.tablefile('spin')
```

... and {func}`tablefiles() <flatspin.data.Dataset.tablefiles>` returns a list of lists:

```{code-cell} ipython3
dataset.tablefiles()
```

(dataset-subset)=
## Selecting parts of a dataset

{class}`Dataset <flatspin.data.Dataset>` offers several methods to select a subset of the runs in a dataset.
These methods return a new {class}`Dataset <flatspin.data.Dataset>` object with a modified `index` containing only the selected subset.

A subset of the dataset can be selected by the IDs in the index:

```{code-cell} ipython3
# Select run with id 3
print(repr(dataset[3]))
print('id =', dataset[3].id())
dataset[3].index
```

```{code-cell} ipython3
# Select a range of runs
dataset[1:3].index
```

It is also possible to {func}`filter <flatspin.data.Dataset.filter>` results based on a column in the index:

```{code-cell} ipython3
dataset.filter(phi=30).index
```

The `n`th row in the index can be obtained with {func}`row(n) <flatspin.data.Dataset.row>`, independently of the run id:

```{code-cell} ipython3
display(dataset[3:].index)
dataset[3:].row(0)
```

## Iterating over a dataset

Iterating over a dataset will generate a dataset object for each row in the index:

```{code-cell} ipython3
for ds in dataset:
    print(repr(ds), ds.row(0)['outdir'])
```

Iterate over `(id, dataset)` tuples with {func}`items() <flatspin.data.Dataset.items>`:

```{code-cell} ipython3
for i, ds in dataset.items():
    print(i, repr(ds))
```

... or over `(row, dataset)` tuples with {func}`iterrows() <flatspin.data.Dataset.iterrows>`:

```{code-cell} ipython3
for row, ds in dataset.iterrows():
    print(row, repr(ds))
```

... or iterate over a column in the index with {func}`groupby() <flatspin.data.Dataset.groupby>`:

```{code-cell} ipython3
for phi, ds in dataset.groupby('phi'):
    print(phi, repr(ds))
```

## Sweeping several parameters

Sweeping several parameters produce more complex datasets.
Below we create a dataset where two parameters are swept: `alpha` and `phi`.
The purpose of the example below is to demonstrate some features of {class}`Dataset <flatspin.data.Dataset>`, so we don't actually run any simulations or save any data.

```{code-cell} ipython3
import itertools
sweep = {
    'alpha': [0.001, 0.002, 0.003],
    'phi': [0, 10, 20, 30, 40],
}
sweep_values = list(itertools.product(sweep['alpha'], sweep['phi']))
sweep_values = np.transpose(sweep_values)

# Create the index table, with one entry per value of phi
alphas = sweep_values[0]
phis = sweep_values[1]
outdirs = [f'run{i:02d}.npz' for i in range(len(phis))]
index = pd.DataFrame({'alpha': alphas, 'phi': phis, 'outdir': outdirs})
display(index)

# Create the dataset object
dataset = Dataset(index)
```

In this case, {func}`filter() <flatspin.data.Dataset.filter>` and {func}`groupby() <flatspin.data.Dataset.groupby>` now returns subsets with several items:

```{code-cell} ipython3
dataset.filter(phi=30).index
```

```{code-cell} ipython3
for alpha, ds in dataset.groupby('alpha'):
    print(alpha)
    print(ds.index)
```

It is also possible to {func}`filter() <flatspin.data.Dataset.filter>` and {func}`groupby() <flatspin.data.Dataset.groupby>` with multiple parameters:

```{code-cell} ipython3
dataset.filter(alpha=0.003, phi=30).index
```

```{code-cell} ipython3
for (alpha, phi), ds in dataset.groupby(['phi', 'alpha']):
    print(alpha, phi, ds.id(), repr(ds))
```

## Further reading

While this guide has introduced the core concepts of the dataset, the {class}`Dataset <flatspin.data.Dataset>` class contains a few extra bells and whistles.
In addition, {mod}`flatspin.data` contains several useful functions for processing simulation results.
