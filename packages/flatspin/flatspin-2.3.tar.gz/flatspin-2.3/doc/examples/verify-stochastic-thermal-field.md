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
```

# Stochastic thermal field
## Verification experiment

In this notebook we set up the flatspin runs and analyse the data for the verification of the stochastic thermal field, as presented in the paper.
In short, we compare flatspin simulations with varying fields and temperatures to experiments where the results are known analytically (or numerically through micromagnetic simulations).

We consider a typical ensemble of uncoupled spins with magnetization direction parallel to an external magnetic field direction.
The ensembles are subject to both temperature and an external field influence.
In the lack of other influences and spin-spin interactions, the ensemble net magnetization is completely defined by temperature and the external field $M(H,T)$.

The experiment has a low coercivity and a high coercivity scenario.
The low coercivity scenario, $h_k$ = 0.001 mT, can be described analytically, by $\langle m_x \rangle = \tanh (A\mu_0 H)$, where $A = M_SV/K_BT)$. The high coercivity scenario, $h_k$ = 0.020 mT, we model by micromagnetic simulations.

+++

### The low coercivity scenario

First, we look at the analytical description of the low coercivity scenario.
We simply plot the following expression for $m_x$:

$\langle m_x \rangle = \tanh (A\mu_0 H)$, where $A = M_SV/K_BT)$,

using the volume and saturation magnetization that we will use in the experiment.

```{code-cell} ipython3
import matplotlib.pyplot as plt
import numpy as np

kB = 1.38064852e-23
msat = 860e3
volume = 10e-9*10e-9*10e-9
temperatures = [100, 300, 500]

def hyptan(msat, V, T, h):
    A = msat * V / (kB * T)
    return np.tanh(A * h)

h_range = np.linspace(-0.025, 0.025, 200) # Unit Tesla, i.e. mu0 * H
for T in temperatures:
    plt.plot(h_range, hyptan(msat, volume, T, h_range), label=f'$T={T}$ K')
    
plt.xlabel('$\mu_0H$ [T]')
plt.ylabel('$m_x$')
plt.legend();
```

Note that this analytical expression does not take into account any coercivty, as it assumes no coercive field.
Therefore, this only applies to the low coercivity scenario.

+++

### Generate flatspin data

To set up the experiment in flatspin, we use the `IsingSpinIce` class, as all the spins are parallel.
`alpha` is set to 0 to isolate each spin, and we use a 16 by 16 spin ensemble, initialized in the negative direction.

Below we build the flatspin-run command by going through the relevant parameters.

```{code-cell} ipython3
from flatspin.model import IsingSpinIce

run_command = 'flatspin-run-sweep -m IsingSpinIce'

alpha = 0
size = (16, 16)

model = IsingSpinIce(alpha=alpha, size=size, init=-1, spin_angle=0)
model.plot()
plt.title('Initial state');

run_command += f" -p alpha={alpha} -p size='{size}' -p init=-1 -p spin_angle=0"
```

We use a quasi-static field protocol, i.e., we increase the field by a small amount and simulate many timesteps at each field value to reach a steady state. We also save the state at each timestep (i.e. `spp = timesteps`).

```{code-cell} ipython3
H_max = 0.1 # Tesla, plenty enough to saturate the ensembles
timesteps_per_H  = 200 # We repeat each field value this many times

H_range = H_max * np.linspace(-1,1,1001) # The number of inputs
H_profile = np.repeat(H_range, timesteps_per_H)

plt.plot(H_profile)
plt.ylabel('$H$ [T]')
plt.xlabel('Step');

run_command += f" -e Constant -p H={H_max} -p 'input=np.linspace(-1,1,1001)'"
run_command += f" -p timesteps={timesteps_per_H} -p spp={timesteps_per_H}"
```

```{code-cell} ipython3
hc_low = 0.001
hc_high = 0.020
delta_t_low = 1e-10
delta_t_high = 1e-9
field_angles = [0]

# Add temperature sweep and other parameters
run_command += f" -s 'temperature={temperatures}' -p msat={msat} -p volume={volume} -p 'm_therm=msat*volume' -s 'phi={field_angles}'"
# Astroid parameters
run_command += " -p sw_b=1 -p sw_c=1 -p sw_gamma=3 -p sw_beta=3"

# Specifiy distributed running on GPUs
run_command += " -p use_opencl=1 -r dist"

# Create one command for the low hc and one for the high hc
run_command_low = run_command + f" -s 'therm_timescale=[{delta_t_low}]' -p hc={hc_low} -o OUTPUT_FILE_LOW" 
run_command_high = run_command + f" -s 'therm_timescale=[{delta_t_high}]' -p hc={hc_high} -o OUTPUT_FILE_HIGH" 

print(run_command_low)
print()
print(run_command_high)
```

The above commands can be used to run and generate {download}`the relevant datasets<temp-verification.zip>`.

+++

### Results

+++

With our data generated, we read the datasets and take a closer look

```{code-cell} ipython3
import pandas as pd
from flatspin.data import Dataset, read_table
from numpy.linalg import norm

# Selected parameters
phi = 0
temperatures = [100,300,500]

# Read data
flatspin_ds_high_hc = Dataset.read('/data/flatspin/temp-verification/temp-verification-high-hc')
flatspin_ds_low_hc = Dataset.read('/data/flatspin/temp-verification/temp-verification-low-hc')

# If the dataset includes extra swept parameters, we filter these out:
flatspin_ds_high_hc = flatspin_ds_high_hc.filter(phi=round(phi), temperature=temperatures, therm_timescale=[1e-9]) 
flatspin_ds_low_hc = flatspin_ds_low_hc.filter(phi=round(phi), temperature=temperatures, therm_timescale=[1e-10])


# Function to return a dataframe with the relevant field and magnetization from a single dataset
def read_hyst_data(ds):
    df = read_table(ds.tablefile("h_ext"), index_col="t")
    df['h'] = np.sign(df["h_extx"]) * norm(df[["h_extx", "h_exty"]].values, axis=1)
    
    # Average magnetization
    spin_states = read_table(ds.tablefile("spin"), index_col="t")
    df["m"] = spin_states.agg('mean', axis=1)
    
    return df
```

We also read in some data that we have generated with micromagnetic simulations.
The data is saved as a csv with the relevant temperature and coercivity (hc). 
The hc field has two values, 'high' and 'low', indicating a coercivity equivalent to hc=0.020 mT and hc=0.001 mT respectively. 
For each external field value, 'B', the average of the binned spin states of each micromagnetic cell, 'sx', is recorded.

```{code-cell} ipython3
mx = pd.read_csv('mumax-temp-vs-field.csv', usecols=['T', 'hc', 'B', 'sx'])
mx = mx[mx['hc'] == 'high'] # The comparison is only valid for the high hc scenario
```

### Plotting everything

We average the magnetization at each field value, and plot everything together.

```{code-cell} ipython3
plt.figure(figsize=(7.08*1.135, 4.395))

H_axis = mx[mx['T']==temperatures[0]]['B']
### high hc subplot ###
plt.subplot(1,2,2)

hc = flatspin_ds_high_hc.params['hc']*1000
plt.title(f'$h_c={hc}$ mT')
plt.xlim(-.025, .025)
plt.xlabel("$\mu_0H$")

for i, T in enumerate(temperatures):
    # Read the temperature dataset
    df = read_hyst_data(flatspin_ds_high_hc.filter(temperature=T))
    # Take the mean for each field value
    df = df.groupby('h').agg('mean').reset_index()
    
    # Plot flatpsin results
    plt.plot(df['h'], df['m'], label=f'$T={T}$ K, flatspin', c=f'C{i}', ls=':' )
    
    # Plot MuMax3 results
    plt.plot(mx[mx['T']==T]['B'], 
             mx[mx['T']==T]['sx'], label=f'$T={T}$ K, MuMax3', c=f'C{i}', ls='--')
    
    # Plot analytical
    ht = hyptan(msat, volume, T, H_axis)
    plt.plot(H_axis, ht, label=f'$T={T}$ K, analytical', ls='-',alpha=0.5, linewidth=2 )

ax = plt.gca()
h, l = ax.get_legend_handles_labels()

### low hc subplot ###
plt.subplot(1,2,1)

hc = flatspin_ds_low_hc.params['hc']*1000
plt.title(f'$h_c={hc}$ mT')
plt.xlim(-.025, .025)
plt.xlabel("$\mu_0H$")
plt.ylabel('$m_x$')

for i, T in enumerate(temperatures):
    df = read_hyst_data(flatspin_ds_low_hc.filter(temperature=T))
    df = df.groupby('h').agg('mean').reset_index()
    
    # Plot flatspin results
    plt.plot(df['h'], df['m'], label=f'$T={T}$ K, flatspin', c=f'C{i}', ls=':')

    # Plot analytical
    ht = hyptan(msat, volume, T, H_axis)
    plt.plot(H_axis, ht, label=f'$T={T}$ K, analytical', ls='-',alpha=0.5, linewidth=2 )


fig = plt.gcf()
fig.subplots_adjust(bottom=0.25, wspace=0.25)
fig.legend(h, l, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=3)

plt.show()
```
