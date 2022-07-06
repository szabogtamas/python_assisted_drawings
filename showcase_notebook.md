---
jupyter:
  jupytext:
    formats: md,ipynb
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# An example plan

## Dependencies

```python
from matplotlib import pylab as plt
from matplotlib import patches as mpl_patches
from matplotlib import cm
```

```python
!pip3 install shapely pysolar
```

```python
import numpy as np
import math
import datetime
from shapely import geometry as sg
from pysolar import solar
```

```python
import sys

sys.path.append("src")  # developmental hack, to load the local version of the module
%load_ext autoreload
%autoreload 2

import pad_draw as dr
```

## Dimensions and locations

```python
object_collection = dict(
    telek = dr.Polygon([(0, 0), (14, 5), (14, 39), (0, 39)]),
    haz = dr.Rectangle(6, 12),
    fenyo = dr.Circle(2),
    mandula = dr.Circle(1),
    terasz = dr.CustomPlatform()
)
```

```python
object_locations = dict(
    telek = (0, 0),
    haz = (1, 24),
    fenyo = (4, 38),
    mandula = (6, 12),
    terasz = (1, 19)
)
```

## Draw plan

```python
for k, v in object_locations.items():
    object_collection[k].update_positions(*v)
```

```python
fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")

for k, v in object_collection.items():
    v.draw(ax)
```

```python
fig.savefig("plan_example.pdf")
```

## Draw Fibonacci spirals

```python
fig, axs = plt.subplots(3, 2, figsize=(7.2, 9.6))
axs = axs.flatten()

experimental_axes = [15, 30, 45, 60, 90, 120]

for i, e in enumerate(experimental_axes):
    axs[i] = dr.draw_fibonacci_spiral(1, 20, e, ax=axs[i])

fig.savefig("fibonacci_spirals.pdf")
```
