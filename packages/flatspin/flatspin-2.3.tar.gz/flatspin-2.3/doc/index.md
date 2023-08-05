---
jupytext:
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
from flatspin.model import *
```

# flatspin
flatspin is a GPU-accelerated simulator for systems of interacting nanomagnet spins arranged on a 2D lattice, also known as Artificial Spin Ice (ASI).
flatspin can simulate the dynamics of large ASI systems with thousands of interacting elements.
flatspin is written in Python and uses OpenCL for GPU acceleration.
flatspin comes with extra bells and whistles for analysis and visualization.

Some example ASI systems are shown below:

```{code-cell} ipython3
:tags: [remove-input]

params = {
    'init': 'random',
    'alpha': 1.0,
    'use_opencl': 1,
    'neighbor_distance': np.inf,
}
model = SquareSpinIceClosed(size=(10,10), **params)
model.relax()
plt.subplot(131)
plt.axis('off')
model.plot()

model = PinwheelSpinIceDiamond(size=(10,10), **params)
model.relax()
plt.subplot(132)
plt.axis('off')
model.plot()

model = KagomeSpinIce(size=(7,9), **params)
model.relax()
plt.subplot(133)
plt.axis('off')
model.plot();

plt.tight_layout();
```

Ready to learn more?
Head over to [](installation) to download and install flatspin.
Then dive into the [](quickstart) to get started using the simulator.

## License and citation
flatspin is open-source software.
You are free to modify and distribute the source-code under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).

flatspin is developed and maintained by an interdisciplinary group of researchers at [NTNU](https://www.ntnu.edu/ie/eecs).
If you use flatspin in any work or publication, we kindly ask you to cite:

[“flatspin: A Large-Scale Artificial Spin Ice Simulator”, Phys. Rev. B 106, 064408 (2022).](https://doi.org/10.1103/PhysRevB.106.064408)

```{literalinclude} flatspin.bib
:language: bibtex
:class: toggle
```
