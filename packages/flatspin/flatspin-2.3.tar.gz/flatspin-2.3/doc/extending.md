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
import matplotlib.pyplot as plt
```

(extending)=

# Extending flatspin

There are many ways to extend the functionality of flatspin.
Here we discuss two of the most common use cases, namely custom geometries and custom encoders.

+++

## Custom geometries

There are two ways to extend flatspin with your own custom geometries:
1. Provide a set of spin positions and angles to {class}`CustomSpinIce <flatspin.model.CustomSpinIce>`
2. Extend {class}`SpinIce <flatspin.model.SpinIce>` and create a parameterized geometry

+++

### Using {class}`CustomSpinIce <flatspin.model.CustomSpinIce>`

{class}`CustomSpinIce <flatspin.model.CustomSpinIce>` can be used to quickly create a custom geometry.
The {class}`CustomSpinIce <flatspin.model.CustomSpinIce>` class accepts a list of positions and angles for all the spins as the parameters `magnet_coords` and `magnet_angles`.

Below we create a geometry on a square lattice in which the spin angles depend directly on their positions.
The parameter `delta_angle` scales the amount of rotation per lattice spacing.

```{code-cell} ipython3
from flatspin.model import CustomSpinIce

# Size (cols, rows) of our geometry
size = (10, 10)

# Positions of spins
lattice_spacing = 1
x = lattice_spacing * np.arange(0, size[0])
y = lattice_spacing * np.arange(0, size[1])
xx, yy = np.meshgrid(x, y)
xx = xx.ravel()
yy = yy.ravel()
pos = np.column_stack([xx, yy])

# Angles of spins
delta_angle = 10
angle = (xx+yy) * delta_angle / lattice_spacing

# Give the angles and positions to CustomSpinIce
model = CustomSpinIce(magnet_coords=pos, magnet_angles=angle, radians=False)
model.plot();
```

While {class}`CustomSpinIce <flatspin.model.CustomSpinIce>` is one way of creating a custom geometry, it is not  parametric.
In other words, any modifications to the geometry must be made manually outside of the class.
Consequently, it is cumbersome to explore variations of this geometry using, e.g., [`flatspin-run-sweep`](flatspin-run-sweep).
In the next section, we will see how to extend flatspin with a new {class}`SpinIce <flatspin.model.SpinIce>` class.

+++

### Extending SpinIce

Fully parametric geometries can be created by creating a subclass of {class}`SpinIce <flatspin.model.SpinIce>`.
Any new parameters should be introduced as keyword arguments to the `__init__` function of the subclass.
The subclass should override {func}`_init_geometry() <flatpsin.model.SpinIce._init_geometry>`, which should return a tuple `(pos, angle)` where `pos` is an array with the positions of the spins, and `angle` is an array with the rotations of the spins.

Below we create a new subclass that provides a fully parametric version of the geometry we created earlier.
We introduce a new parameter `delta_angle`, while `size` and `lattice_spacing` are already defined by the {class}`SpinIce <flatspin.model.SpinIce>` base class.

```{code-cell} ipython3
from flatspin.model import SpinIce

class MySpinIce(SpinIce):
    def __init__(self, *, delta_angle=10, **kwargs):
        self.delta_angle = delta_angle

        super().__init__(**kwargs)

    def _init_geometry(self):
        # size and lattice_spacing are SpinIce parameters
        size = self.size
        lattice_spacing = self.lattice_spacing

        # positions of spins
        x = lattice_spacing * np.arange(0, size[0])
        y = lattice_spacing * np.arange(0, size[1])
        xx, yy = np.meshgrid(x, y)
        xx = xx.ravel()
        yy = yy.ravel()
        pos = np.column_stack([xx, yy])

        # angles of spins
        delta_angle = np.deg2rad(self.delta_angle)
        angle = (xx+yy) * delta_angle / lattice_spacing

        # Generate labels for our geometry (optional)
        #self.labels = grid

        return pos, angle

    # The size of vertices in our geometry (optional)
    _vertex_size = (2, 2)
```

With our new `MySpinIce` class, we are ready to explore the parameter space:

```{code-cell} ipython3
for i, delta_angle in enumerate([0, 30, 60, 90]):
    model = MySpinIce(size=(10,10), delta_angle=delta_angle)
    plt.subplot(1, 4, i+1)
    plt.title(f"{delta_angle}")
    plt.axis('off')
    model.plot()
```

## Custom encoders

An [encoder](encoders) translates logical input to an external field protocol.

Input takes the form of arrays of shape `(n_inputs, input_dim)`.
1D input arrays may be used as a shorthand for `(n_inputs, 1)`.

The encoding process consists of one or more steps, where the output of one step is input to the next step:

`input -> step1 -> step2 -> ... -> h_ext`

In general, signals can take any shape as part of the encoding process.
However, the last step must produce an output of either:

1. `(time, 2)`: a global vector signal
2. `(time, H, W, 2)`: a local vector signal on a grid

Each step is a simple function taking a single `input` argument, and any number of parameters as keyword arguments:

```python
def step(input, param1=default1, param2=default2, ...):
    ...
```

```{note}
The only non-keyword argument to a step function is `input`.
Parameters are only allowed as keyword arguments, and **must** have default values.
```

The {class}`Encoder <flatspin.encoder.Encoder>` will inspect the signature of each step to discover the available parameters.
The parameters can then be set during encoder initialization, or afterwards via {func}`set_params() <flatspin.encoder.Encoder.set_params>`.
Note that parameter names may overlap, in which case all matching parameters will be set to the same value.

Custom encoders can be created by subclassing {class}`Encoder <flatspin.encoder.Encoder>` and provide a list of `steps`.

Below we create a custom encoder where:
1. Input is encoded as the amplitude of a global external field
2. For each input, the angle of the field is incremented by a fixed amount `delta_angle`

```{code-cell} ipython3
from flatspin.encoder import Encoder

def scale_step(input, H=1):
    return H * input

def rotate_step(input, delta_angle=15):
    n_inputs = len(input)
    angles = np.arange(0, delta_angle * n_inputs, delta_angle)
    angles = np.deg2rad(angles)
    h_ext = input * np.column_stack([np.cos(angles), np.sin(angles)])
    return h_ext

class MyEncoder(Encoder):
    steps = [scale_step, rotate_step]
```

The two steps (1) and (2) are implemented by the functions `scale_step` and `rotate_step`, respectively.
The steps are tied together in the new `MyEncoder` class.

```{code-cell} ipython3
# Encoder automatically discovers the available parameters from the kwargs of the steps
encoder = MyEncoder()
print(encoder.get_params())
```

```{code-cell} ipython3
# Linear input from 0..1
input = np.linspace(0, 1, 50, endpoint=False)
h_ext = encoder(input)

# Scatter plot of h_ext, where color indicates time
plt.title('h_ext')
plt.scatter(h_ext[:,0], h_ext[:,1], c=np.arange(len(h_ext)), marker='.', cmap='plasma')
plt.axis('equal')
plt.colorbar(label='time');
```

```{code-cell} ipython3
# Four periods of a sine wave, scaled to the range 0.5..1
input = np.linspace(0, 1, 360, endpoint=False)
input = np.sin(-np.pi/2 + 8*np.pi*input)
input = 1/2 + input/2

plt.figure()
plt.title('input')
plt.plot(input)

encoder.set_params(delta_angle=360/len(input))
h_ext = encoder(input)

plt.figure()
plt.title('h_ext')
plt.scatter(h_ext[:,0], h_ext[:,1], c=np.arange(len(h_ext)), marker='.', cmap='plasma')
plt.axis('equal')
plt.colorbar(label='time');
```

The {mod}`flatspin.encoder` module contains a range of useful encoder steps.
In fact, it already includes a step called {func}`scale <flatspin.encoder.scale>` which is functionally equivalent to our custom `scale_step` above, but with an additional parameter `H0` to specify an offset, so that the input is scaled from `H0..H`.

```{code-cell} ipython3
from flatspin.encoder import scale

class MyEncoder2(Encoder):
    steps = [scale, rotate_step]

encoder2 = MyEncoder2(delta_angle=360/len(input), H0=0.5, H=1.0)
h_ext = encoder2(input)

plt.title('h_ext')
plt.scatter(h_ext[:,0], h_ext[:,1], c=np.arange(len(h_ext)), marker='.', cmap='plasma')
plt.axis('equal')
plt.colorbar(label='time');
```

## Using custom models and encoders from the command-line

The [command-line tools](cmdline) [`flatspin-run`](flatspin-run) and [`flatspin-run-sweep`](flatspin-run-sweep) support the use of custom models and encoders.

To use your own model class, simply provide the full module path to `-m/--model`.
Similarly, to use your own encoder class, provide the full module path to `-e/--encoder`.
Any custom parameters can be set as usual with `-p/--param`.

For example, placing the `MySpinIce` class in a file `mymodels.py`, and `MyEncoder` in a file `myencoders.py`, we can do:

```bash
flatspin-run -m mymodels.MySpinIce -p delta_angle=30 ... -e myencoders.MyEncoder -p [TODO]
```
