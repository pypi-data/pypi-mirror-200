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

(annealing)=

# Thermal annealing

## Domain size in square ASI

In section V. B. of our paper {cite}`Flatspin2022`, we briefly describe the use of flatspin to perform an annealing procedure to match an experimental setup.
The following is the setup for flatspin's parameters and a guide to how the experiment was performed.
This example demonstrates a large part of flatspin's features, and most notably a novel use of its temperature implementation. 

The main goal of this experiment is to reproduce the annealing of square artificial spin ice, as in {cite}`Zhang2013`

[“Crystallites of magnetic charges in artificial spin ice” Nature, vol. 500, no. 7464, 553–557 (2013)](https://doi.org/10.1038/nature12399).

There are six main parts to this experiment:

1. Define the systems temperature dependent parameters
2. Define the probablities of flipping once (and more) for a given simulation step
3. Use the probabilities and temperature dependent parameters to identify the nucleation volume
4. Derive an annealing profile and generate the parameters.
5. Produce the flatspin run command and input files
6. Results

+++

## 1. Temperature dependent parameters

At high temperatures, the physical magnetic materials constituting the nanomagnet dipoles change their physical properties. While these material properties are not directly modeled by flatspin, we can change relevant parameters of the simulation to fit the temperature induced change. 

**Saturation magnetization,  $M_\text{S}(T)$**  
One of the most important changes to a magnetic material as you heat it is the reduction of saturation magnetization. We use values obtained for a 25 nm permalloy film to find an expression for $M_\text{S}(T)$.
The {download}`experimental values <Zhang-Py-25nm-msat-vs-T.json>` are gathered from {cite}`Zhang2019`.

```{code-cell} ipython3
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from functools import partial

# Some constant we will use later
mu0 = 1.256637e-6 # kg m s^-2 A^-2
kB = 1.38064852e-23 # m^2 kg s^-2 K^-1 

# Open the data from Zhang2019
with open('Zhang-Py-25nm-msat-vs-T.json') as f:
    msat_data = json.load(f) 
dataset_zfc = [dataset['data'] for dataset in msat_data['datasetColl'] if dataset['name']=='ZFC'][0]
data = [p['value'] for p in dataset_zfc]    
x, y = list(zip(*data))
y = [val*1e3 for val in y] # Convert to units of A/m
# Plot it
plt.figure(dpi=100)
plt.scatter(x, y, c = 'r',  s = 3, label='Extracted data')

# Fit the following function to the msat curve
def f1(x, a, b, c): 
    return -a*np.log(-b/(x-c))
a1, b1, c1 = 150000, 10, 820 # Some rough fitting parameters as initial guess
(a0, b0, c0), _ = optimize.curve_fit(f1,  x,  y,  p0=(a1, b1, c1))
x_ax = np.linspace(min(x), max(x))
plt.plot(x_ax, f1(x_ax, a0, b0, c0), label = '$M_S(T)$ Curve fit')

plt.xlabel('Temperatue [K]')
plt.ylabel('Saturation magnetization [A/m]')

# Create the msat(T) function, units A/m (not kA/m, as in Zhang et al.)
msat_vs_T = partial(f1, a=a0, b=b0, c=c0)
plt.legend();
```

**Coupling strength,  $\alpha$**  
While $M_\text{S}(T)$ is not a direct part of flatspin, it influences other parameters relevant for flatspin simulations. One of these are the coupling parameter, $\alpha$, which we can define given an $M_\text{S}(T)$, a volume and a lattice spacing. 

**Switching threshold, $h_c$**  
As the saturation magnetization varies, so does the switching threshold, $h_c$. 
We create a function to estimate the switching threshold from the temperature, using our `msat_vs_T` function.  
*The coefficients of the scaling is taken from micromagnetic simulations.*

```{code-cell} ipython3
# Calculate alpha (in Tesla)
def alpha_calc(msat, V, a):
    return mu0 * msat * V / (4 * np.pi * a**3)

# Calculate switching threshold 
def hc_vs_T(T, msat=None):
    coeff = np.array([2.36501465e-07, -8.52767576e-03]) 
    if msat is None:
        msat = msat_vs_T(T)
    return np.polyval(coeff, msat)
```

Below is a plot of the calculated $\alpha$ values and $h_c$ values for magnets of size $220\times80\times25$ nm and a separation of $320$ nm.

```{code-cell} ipython3
:tags: [hide-input]

T_range = np.linspace(300,820,500)
volume =  220e-9 * 80e-9 * 25e-9
separation = 320e-9

# Plot alpha
plt.figure(dpi=100)
plt.plot(T_range, alpha_calc(msat_vs_T(T_range), volume, separation), c='C0', ls='-', linewidth=2, label='alpha')
plt.ylabel('Coupling coefficient, alpha, [T]')
plt.xlabel('Temperature [K]')
plt.legend(loc='upper right', bbox_to_anchor=(1, 1.0))

# Plot hc
ax2 = plt.gca().twinx()
ax2.plot(T_range, hc_vs_T(T_range), c='C1', ls=':', lw=4, label='hc')
plt.ylabel('Switching threshold, hc [T]')
plt.legend(loc='upper right', bbox_to_anchor=(1, 0.9));
```

## 2. Flipping probabilities

We now use the temperature dependent parameters to define functions returning the probability of switching in a given scenario. 
The probability is evaluated for an unbiased magnet, i.e., we consider the shortest distance to the astroid edge from the origin.
To calculate this, we use an example model instance with the same parameters as in the simulation we will be doing, and use its `_zero_to_astroid` attribute. 
We use the Poisson formula to calculate the probability.

The `_zero_to_astroid` attribute returns the smallest field required to flip a magnet, **in units of $h_c$**, which we can use to multiply by `hc_vs_T(T)` to get the smallest field required to flip an unbiased magnet. Thus, only the astroid parameters, `sw_b`,  `sw_c`, `sw_beta`, and `sw_gamma`, are relevant for the example model instance. 

We define the probability of flipping *at least once*, `P_flip`, and the probability of flipping *more than once*, `P_multiflip`.

```{code-cell} ipython3
from flatspin.model import SquareSpinIceClosed

# Example model instance
model = SquareSpinIceClosed(sw_b=0.38, sw_c=1.0, sw_beta=1.3, sw_gamma=3.6)

def P_flip(T, delta_t, volume_nuc):
    threshold_zero = model._zero_to_astroid * hc_vs_T(T)
    attempt_freq = model.attempt_freq
    m_therm = msat_vs_T(T) * volume_nuc
    
    # Poisson rate
    f = attempt_freq * np.exp(-m_therm * threshold_zero / (kB * T))
    P_flip_zero = np.exp(-f * delta_t)
    
    return 1 - P_flip_zero

def P_multiflip(T, delta_t, volume_nuc):
    threshold_zero = model._zero_to_astroid * hc_vs_T(T)
    attempt_freq = model.attempt_freq
    m_therm = msat_vs_T(T) * volume_nuc
    
    # Poisson rate
    f = attempt_freq * np.exp(-m_therm * threshold_zero / (kB * T))
    P_flip_zero = np.exp(-f * delta_t)
    P_flip_once = f * delta_t * np.exp(-f * delta_t)
    P_multiflip = 1 - P_flip_zero - P_flip_once
    
    return P_multiflip
```

### The challenge of choosing delta_t

Below is a visualization of the probability of flipping once, P_flip, and more than once, P_multiflip, as a function of temperature and simulation time interval.
The example is for a magnet of size  $220\times80\times25$ nm, assuming a 5% nucleation volume.

At high temperatures (~800 K), the maximum simulation time interval that would keep P_multiflip below an acceptable value is about 10e-8 seconds.
We see that continuous simulation from high temperatures to room temperature is difficult to do without changing the simulation time interval.
A naive approach could be to stay at a low delta_t throughout all temperatures, but this would hardly simulate any physical time at all (each step accounting for 10e-8 seconds).
Instead we can increase the time intervals as we decrease temperature, as long as we stay below an accepted value of P_multiflip.
We call this process the "annealing profile" and in [](annealing-profile) we will have a closer look at how we go about choosing the right one for this experiment.

```{code-cell} ipython3
:tags: [hide-input]

# === First plot: heatmap of P_flip(T, delta_t) ===
plt.figure(dpi=100)
plt.subplot(121)
# Range over which to plot P_flip and P_multiflip
delta_t_range = np.geomspace(1e-10,1e10,500)
T_range = np.linspace(500,820,500)
volume =  220e-9 * 80e-9 * 25e-9

# Calculate the probability heatmap of T and delta_t
Tv, dtv = np.meshgrid(T_range, delta_t_range)
T_v_dt_flip = P_flip(Tv, dtv, volume_nuc=volume*0.05)
T_v_dt_multiflip = P_multiflip(Tv, dtv, volume_nuc=volume*0.05)

# Show the probablity heatmap
plt.pcolormesh(T_range, np.log10(delta_t_range), T_v_dt_flip, shading='auto', rasterized=True)
plt.ylabel(r'$\log(\Delta t~[s])$')
plt.xlabel(r'$T [K]$')
plt.title('P_flip')

# === Second plot: heatmap of P_flip(T, delta_t) ===
plt.subplot(122)

# Range over which to plot P_flip and P_multiflip
delta_t_range = np.geomspace(1e-10,1e10,500)
T_range = np.linspace(500,820,500)

# Calculate the probability heatmap of T and delta_t
Tv, dtv = np.meshgrid(T_range, delta_t_range)
T_v_dt_multiflip = P_multiflip(Tv, dtv, volume_nuc=volume*0.05)

# Show the probablity heatmap
plt.pcolormesh(T_range, np.log10(delta_t_range), T_v_dt_multiflip, shading='auto', rasterized=True)
plt.xlabel(r'$T [K]$')
plt.title('P_multiflip')
plt.colorbar();
```

## 3. Nucleation moment, $M_{th}$

Now that we have the probabilities of flipping we can tune the final parameter, the nucleation moment, to fit with an expected (lack of) activity as described in {cite}`Zhang2019`.
We expect the magnets to not flip at all below $T=673$ K, and we use this to define the nucleation volume (and thus the nucleation moment, $M_{th}$, to be used by flatspin). Thus we set `P_desired_flip = 0.00001` at timestep length `dt_freeze = 60` and temperature `T_freeze = 673`.

```{code-cell} ipython3
T_freeze = 673 # kelvin
dt_freeze = 60 # If nothing happens in 60 seconds, we say the magnets are frozen
P_desired_flip = 0.00001 # At freeze out, we want flips to be unlikely

# ==== Find nucleation volume ====
# First, create a f(nuc_volume) that we can evaluate against P_desired_flip
volume = 220e-9*80e-9*25e-9 # The actual volume of the magnets

def P_flip_from_V_nuc(V_nuc):
    return P_flip(T_freeze, dt_freeze, volume_nuc=V_nuc)

# Plot P(nuc_volume) over the relevant nuc_volume range
plt.figure(dpi=100)
# We assume here that the interesting part will be for volumes less than half the total volume
nuc_fractions = np.linspace(0.01,0.5,1000)
plt.plot(nuc_fractions, P_flip_from_V_nuc(nuc_fractions*volume), label='P_flip = f(nuc_volume)')
plt.xlabel('Nucleation volume fraction')
plt.ylabel('P_flip')

# Plot the target, P_desired_flip
plt.plot(nuc_fractions, [P_desired_flip]*len(nuc_fractions), label='P_flip, target')

# ==== Do bisection of P_flip_from_V_nuc to find the desired value ====
# First create the function to search for roots
def P_flip_min_desired(nuc_fraction):
    return (P_flip_from_V_nuc(nuc_fraction*volume)-P_desired_flip)
plt.plot(nuc_fractions, P_flip_min_desired(nuc_fractions), label='Root searching function')

# Search for roots
nuc_vol_fraction = optimize.bisect(P_flip_min_desired, 0, 1, disp=True)
volume_nuc = nuc_vol_fraction*volume

# Print results
print(f'Found nuc volume:\n {volume_nuc} out of {volume},\nnuc_fraction = {nuc_vol_fraction}')
plt.scatter(nuc_vol_fraction, P_flip_from_V_nuc(volume_nuc), c='r', label='Identified nucleation volume')
plt.legend()
plt.ylim((-2*P_desired_flip,P_desired_flip*50))
plt.title('T = 673 K, delta_t = 60 s');
```

(annealing-profile)=
## 4. Annealing profile

We are now ready to look at the effects of changing the timestep length and temperature, and use this to find a suitable annealing protocol.

Ideally, we would do just like in the experiment {cite}`Zhang2013`, decreasing by 1 minute per kelvin, starting at `T_max = 800` kelvin, simulated as a single step per temperature value.T
If `P_multiflip` rises above the accepted `multiflip_threshold`, we must reduce the timestep length and do more, shorter steps at these temperatures.

We will see that this approach is a bit too naive.

```{code-cell} ipython3
# === The "ideal" annealing profile ===
multiflip_threshold = 0.001
dt_cap = 60

# === Plot: heatmap of P_flip(T, delta_t) ===
plt.figure(dpi=100)

# Range over which to plot P_flip and P_multiflip
delta_t_range = np.geomspace(1e-10,1e10,500)
T_range = np.linspace(500,820,500)

# Calculate the probability heatmap of T and delta_t
Tv, dtv = np.meshgrid(T_range, delta_t_range)
T_v_dt_multiflip = P_multiflip(Tv, dtv, volume_nuc=volume_nuc)

# Show the probablity heatmap
plt.pcolormesh(T_range, np.log10(delta_t_range), T_v_dt_multiflip, shading='auto', rasterized=True)
plt.ylabel(r'$\log(\Delta t)$')
plt.xlabel(r'$T [K]$')    
plt.title('P_multiflip')
plt.colorbar()

# Plot "freeze out cursor", i.e., where we expect the magnets to be stable
plt.axvline(T_freeze, c='c', label=f'T = {T_freeze} K (blocking temp)')
plt.axhline(np.log10(dt_cap), c='C1', label=f'delta_t = {dt_cap} s')

# Find T and delta_t where P_multiflip == multiflip_threshold
# For now, we create a delta_t(T) function from this contour object,
# in the next section we will derive it properly.
cs = plt.contour(T_range, np.log10(delta_t_range), T_v_dt_multiflip, [multiflip_threshold], colors='r')
cs.collections[0].set_label(f'P_multiflip = {multiflip_threshold}')
p = cs.collections[0].get_paths()[0]
v = p.vertices

# Plot the "ideal" temperature profile
T_ideal = np.arange(800, T_freeze, -1)
dt_ideal = np.minimum(np.repeat(np.log10(dt_freeze), len(T_ideal)), np.interp(T_ideal, v[:,0], v[:,1]))
plt.plot(T_ideal, dt_ideal, c='C2', label = '"Ideal" temperature profile')
plt.scatter(*[(min(T_ideal), max(T_ideal)),(max(dt_ideal), min(dt_ideal))], c='C2')

plt.legend(loc='upper left', bbox_to_anchor=(1.2, 1.0));
```

Implementing the above temperature profile, with the goal of simulating one minute at each degree kelvin would require about 10^10 steps, just for the $T = 800$ K step. 
To make our simulation feasible, we abandon the hope of simulating a full minute at all temperatures, and settle on a fixed number of simulation step per temperature. 
For the lower temperatures, we end up simulating at the desired 1 minute per kelvin, but at higher temperatures this compromise simulates less actual time.
However, with enough simulation steps and high switching frequencies we assume that we do not miss important dynamics. 

To create this compromise temperature profile, it will be useful to calculate the maximum timestep length we can do without violating a certain `P_flip` or `P_multiflip` requirement.  
Below we create a function to yield the maximum timestep length and calculate a temperature profile.

```{code-cell} ipython3
from scipy.special import lambertw
from numpy import real

# === First we create a way to calculate the maximum delta_t ===
def calc_delta_t(T, m_therm, delta_h, P_flip=None, P_multiflip=None, f0=1e9):
    """ Calculate maximum delta_t for target P_flip or P_multiflip.
        Returns the delta_t that would result in a probability that is
        smaller than (or equal to) the one supplied.
    """
    f = f0 * np.exp(-m_therm * delta_h / (kB * T))
    if P_flip is not None:
        assert P_multiflip is None
        # Using the equation for of flipping at least once,
        # 1 - np.exp(-f * delta_t),
        # and solving for delta_t is straight forward
        return np.log(1 - P_flip)/-f
    
    elif P_multiflip is not None:
        assert P_flip is None
        # Using the expression for the likelihood of multiple switching events,
        # 1 - np.exp(-f * delta_t) - f * delta_t * np.exp(-f * delta_t),
        # to solve for delta_t is not trivial.
        # We do so here by using the Lambert W function from scipy.
        return real((1/f)*(-lambertw((P_multiflip - 1)/np.exp(1), -1) - 1))
        
    raise ValueError("Need either P_flip or P_multiflip")
    
def max_delta_t(T, P_flip=None, P_multiflip=None):
    delta_h = model._zero_to_astroid * hc_vs_T(T)
    f0 = model.attempt_freq
    msat = msat_vs_T(T)
    m_therm = msat * volume_nuc
    return calc_delta_t(T, m_therm, delta_h, P_flip, P_multiflip, f0)

# === Return the temperatures, delta_ts, number of timesteps, 
# and temperature where 1 min/K is reached (T_breakoff)
def make_fixed_temperature_profile(T_max, T_min, timesteps_per_K, multiflip_threshold, max_tpk=60):
    Ts = np.arange(T_max, T_min-.1, -1)
    max_dt = max_tpk / timesteps_per_K
    dts = max_delta_t(Ts, P_multiflip=multiflip_threshold)
    T_breakoff = Ts[np.argmax(dts > max_dt)]
    dts[dts>max_dt] = max_dt
    ns = np.repeat(timesteps_per_K, len(Ts))

    return Ts, dts, ns, T_breakoff
                         
T_max = 800
timesteps_per_K = 50
Ts, dts, ns, T_breakoff = make_fixed_temperature_profile(T_max, T_freeze, timesteps_per_K, multiflip_threshold)
time_per_kelvin = ns * dts

print(f"Temperature range to be simulated  at less than {np.max(time_per_kelvin)} seconds: {T_max} - {T_breakoff}")
print(f"Time per kelvin range: {np.min(time_per_kelvin)} - {np.max(time_per_kelvin)}")
print(f"Total timesteps: {sum(ns)}")
# print("Ts =", Ts)
# print("ns =", ns)
# print("dts =", dts)
# print("ns * dts=", time_per_kelvin)
```

```{code-cell} ipython3
# === Plot everything ===
# Plot the temperature profile in the P_flip heatmap
plt.figure(dpi=100)
plt.subplot(1,1,1)
T_v_dt = P_flip(Tv, dtv, volume_nuc=volume_nuc)
plt.pcolormesh(T_range, np.log10(delta_t_range), T_v_dt, shading='auto', rasterized=True)

# T_freeze line
plt.axvline(T_freeze, label='T_freeze', color='c')

#for T_max in np.arange(740, 821, 10):
Ts, dts, ns, T_breakoff = make_fixed_temperature_profile(T_max, T_freeze, timesteps_per_K, multiflip_threshold)
tpk = ns * dts
plt.plot(Ts, np.log10(dts), c='C2', label='Timestep length')
plt.scatter([Ts[0], Ts[-1]], [np.log10(dts[0]), np.log10(dts[-1])], c='C2')

plt.ylabel(r'$\log10(\Delta t)$')
plt.xlabel(r'$T$ [K]')    
plt.title('P_flip')
plt.colorbar()
plt.plot(Ts, np.log10(ns*dts), c='C1', label='Total time per $T$')
plt.axhline(np.log10(60), c='C1', ls=':', label=f'{dt_freeze} seconds')
plt.legend(loc=(0.04,0.04));
```

In the above plot, we show the timestep length of the annealing profile (green). 
Starting at $T = 800$ K, and cooling down, the timestep length is gradually increased until the total simulated time at each temperature reaches 60 seconds. The timestep length is then kept constant (as the total simulated time per temperature stays at 60 seconds), until `T_freeze`.

+++

## 5. flatspin run command and input files

Now that we have our parameter arrays, we can generate a command to run the experiment.
We will dump the parameters to CSV files and create the command in accordance with the other parameters outlined in the experiment {cite}`Zhang2013`.

```{code-cell} ipython3
import os
from flatspin.data import save_table

# === Save params.csv ===
# Output files  
root_dir = "params_folder"
params_path = root_dir + "/params.csv"
if not os.path.exists(root_dir):
    os.makedirs(root_dir)
    print(f"Creating directory {root_dir}")

# === Define the relevant model parameters (not temperature dependent) ===
# Commented out parameters are normally supplied, but are here replaced by sweeping parameters.
params = dict(
    size=(50, 50),
#     alpha=alpha_calc(msat = msat_vs_T(300), V = volume, a = 1e-9),
    neighbor_distance=10,
#     hc=hc0,
    disorder=0.05,
    sw_b=0.38, sw_c=1.0, sw_beta=1.3, sw_gamma=3.6,
#     m_therm=msat * volume_nuc,
    use_opencl=1,
    H=0, spp=1, timesteps=1,
)

print(f"Saving static params to {params_path}")
save_table(params, params_path)
```

```{code-cell} ipython3
import pandas as pd
# === Save temperature dependent parameters and genereate command with all lattice spacings ===
lattice_spacings = [320, 360, 400, 440, 480, 560, 680, 880]

# Temperature dependent parameters
# All are technically a function of time, hence the '_t' subscript
Ts_out = np.repeat(Ts, ns)
dts_out = np.repeat(dts, ns)
msats = msat_vs_T(Ts_out)
alphas = alpha_calc(msats, volume, 1e-9)
m_therms = msats*volume_nuc
hcs_out = hc_vs_T(Ts_out)

csvs = [
    ('temperature_t', Ts_out),
    ('therm_timescale_t', dts_out),
    ('alpha_t', alphas),
    ('m_therm_t', m_therms),
    ('hc_t', hcs_out),
]

index = dict()
for k, v in csvs:
    filename = f"{k}.csv"
    filepath = root_dir + "/" + filename
    print(f"Creating {filepath}")
    np.savetxt(filepath, v)
    index[k] = filepath

# Parameters it is nice to keep track off, but which are not part of the model are also saved in the index
index["T_max"] = T_max
index["T_breakoff"] = T_breakoff
index["T_min"] = T_freeze
index["multiflip_threshold"] = multiflip_threshold
index["periods"] = len(Ts_out)

index = pd.DataFrame([index])
index = index.reindex(index.index.repeat(len(lattice_spacings))).reset_index(drop=True)
index.insert(loc=0, column='lattice_spacing', value=lattice_spacings)

print(f"Generated {len(index)} runs")
display(index)

index_file = "index.csv"
index_path = root_dir + "/" + index_file
print(f"Saving index to {index_path}")
save_table(index, index_path)

# Generate flatspin-run-sweep command
print("\nGENERATED COMMAND: \n")
print(f"flatspin-run-sweep -r dist -m SquareSpinIceClosed -e Sine ", end='')
print(f"--params-file={params_path} --sweep-file={index_path} ", end='')
print("-o CHANGE_TO_OUTPUT_FOLDER") # The folder to create the 
```

**We are now ready to run the above command!**

Remember to upload the `params-file` (`params.csv`) and the `sweep-file` (`index.csv`) to the file location you run flatspin from. 

Notes: 

 - The `-r dist` flag tells flatspin to run distributed on a cluster. Skip this if you just run this locally. 
 - The `-e Sine` flag signifies the use of a sine encoder for the external field, but there is no input in this experiment. This flag is there to satisfy the requirement of providing an encoder to flatspin runs, but will have noe effect since there's no input and the field is set to zero with the `H=0` parameter.

+++

### 6. Results

We have our results. Now, let's have a look!  
Below we define a function to read out the spin state of any timestep from our resulting files. We can use this to animate the timeseries of the annealing process.

```{code-cell} ipython3
from flatspin.data import Dataset, read_table, read_geometry, read_vectors, vector_grid
from flatspin.grid import Grid
from flatspin.vertices import find_vertices, vertex_pos, vertex_mag
from flatspin.plotting import plot_vectors, plot_vector_image


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
```

#### Read the datasets

This might take some time.

```{code-cell} ipython3
# Read the dataset
dataset = Dataset.read('/data/flatspin/annealing-example-run')
dataset = dataset.filter(multiflip_threshold=multiflip_threshold, periods=len(Ts_out))

# Read the states of the vertices at specified timesteps
# (read at the end of each temperature step)
periods = len(Ts_out)
ts = np.arange(timesteps_per_K -1, periods, timesteps_per_K)
vertex_states = dict()
for ls, ds in dataset.groupby('lattice_spacing'):
    vertex_states[ls] = read_data_vertices_grid(ds, t=ts)
```

#### Plot the final frame

```{code-cell} ipython3
def plot_vertices(XY, UVi, ax):
    ax.axis('off')
    plot_vector_image(XY, UVi, ax=ax, replace=True)

fig, axs = plt.subplots(2, 4, figsize=(12,6), dpi=200)
for ax, (ls, vstate) in zip(axs.flat, vertex_states.items()):
    ax.set_title(f'lattice spacing = {ls} nm')
    XY, UVi = vstate
    mag = np.amax(np.linalg.norm(UVi[-1], axis=-1))
    plot_vertices(XY, UVi[-1]/mag, ax)
fig.suptitle('Final timestep', fontsize='x-large');
```

#### Animate over all temperatures

```{code-cell} ipython3
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

num_frames = periods // timesteps_per_K
temperatures = list(read_table(dataset.tablefiles('params_t')[0][0])['temperature'][timesteps_per_K-1::timesteps_per_K])
def animate_annealing(vstates):
    # Set up figure and axes
    fig, axs = plt.subplots(2, 4, figsize=(12,6), dpi=200)
    for ax, (ls, vstate) in zip(axs.flat, vstates.items()):
        ax.set_title(f'lattice spacing = {ls} nm')
    
    def do_plot(t):
        fig.suptitle(f'T = {temperatures[t]} K', y=0.0, va='bottom', fontsize='xx-large')
        for ax, (ls, vstate) in zip(axs.flat, vstates.items()):
#             ax.set_title(f'lattice spacing = {ls} nm')
            XY, UVi = vstate
            mag = np.amax(np.linalg.norm(UVi[-1], axis=-1))
            plot_vertices(XY, UVi[t]/mag, ax)
    
    anim = FuncAnimation(fig, do_plot, frames=num_frames, interval=150, blit=False)
    plt.close() # Only show the animation
    #anim.save("astroid.gif")
    return HTML(anim.to_jshtml())
```

```{code-cell} ipython3
animate_annealing(vertex_states)
```
