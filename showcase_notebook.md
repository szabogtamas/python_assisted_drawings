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
import numpy as np
import math
import datetime

from pysolar import solar
```

## Define artist objects

```python
class Rectangle:
# A most basic artist, a rectangle that will also be building block of other objects

    def __init__(
        self, width, height, angle=0, color="k", ls="-", lw=0.1,
        fill=False, alpha=1, z=2, sun_h=None, sun_a=None, sun_r=None,
        shadow_color="#D3D3D3", shadow_only=False
    ):
        self.x = 0
        self.y = 0
        self.z = z
        self.w = width
        self.h = height
        self.angle = angle
        self.color = color
        self.ls = ls
        self.lw = lw
        self.fill = fill
        self.alpha = alpha
        self.shadow_color = shadow_color
        self.shadow_only = shadow_only
        if sun_h is None:
            if 'SUN_ALT' in globals():
                self.sun_h = SUN_ALT
            else:
                self.sun_h = 20
        else:
            self.sun_h = sun_h
        self.sun_tn = self.z/math.tan(math.radians(SUN_ALT))
        if sun_r is None:
            if 'SUN_ROT' in globals():
                self.sun_r = SUN_ROT
            else:
                self.sun_r = 20
        else:
            self.sun_r = sun_r
        if sun_a is None:
            if 'SUN_AZY' in globals():
                self.sun_a = SUN_AZY + self.sun_r
            else:
                self.sun_a = 20
        else:
            self.sun_a = sun_a
    
    def update_positions(self, x, y):
        self.x = x
        self.y = y

    def initialize_geometry(self):
        p = mpl_patches.Rectangle(
            (self.x, self.y), self.w, self.h,
            color=self.color, ls=self.ls, fill=self.fill, lw=self.lw
        )
        return p

    def draw(self, ax):
        ax.add_patch(self.initialize_geometry())
        return ax

# Consider using something like https://lerner.co.il/2014/01/03/making-init-methods-magical-with-autoinit/ later
```

```python
class Circle(Rectangle):
# A primitive artist, an empty circle

    def __init__(self, r, color="k", ls="-", lw=0.1, fill=False):
        self.x = 0
        self.y = 0
        self.r = r
        self.color = color
        self.ls = ls
        self.lw = lw
        self.fill = fill        

    def initialize_geometry(self):
        p = mpl_patches.Circle(
            (self.x, self.y), self.r,
            color=self.color, ls=self.ls, fill=self.fill, lw=self.lw
        )
        return p
```

```python
class Polygon(Rectangle):
# A primitive artist, a custom polygon

    def __init__(self, point_aray, color="k", ls="-", lw=0.1, fill=False):
        self.points = point_aray
        self.color = color
        self.ls = ls
        self.lw = lw
        self.fill = fill
    
    def update_positions(self, x, y):
        self.points =  [(dx+x, dy+y) for dx, dy in self.points]  

    def initialize_geometry(self):
        p = mpl_patches.Polygon(
            self.points,
            color=self.color, ls=self.ls, fill=self.fill, lw=self.lw
        )
        return p
    
    def initialize_shadow(self):
        pl = []
        for i, (xp1, yp1) in enumerate(self.points):
            xp2, yp2 = self.points[i-1]
            p = mpl_patches.Polygon(
                [
                    (xp1, yp1), (xp2, yp2),
                    self.rotate_edge((xp2, yp2+self.sun_tn), (xp2, yp2), self.sun_a),
                    self.rotate_edge((xp1, yp1+self.sun_tn), (xp1, yp1), self.sun_a)
                ],
                color=self.shadow_color, fill=True, alpha=0.1
            )
            pl.append(p)
        return pl
```

```python
class CustomPlatform(Polygon):
# A composite object built up of multiple primitves

    def __init__(self, color="k", ls="-", lw=0.1, fill=False):
        self.color = color
        self.ls = ls
        self.lw = lw
        self.fill = fill
        self.points = [
            (0.2, 0.2),
            (2.9, 0.2),
            (0, 0),
            (0, 5),
            (6, 5),
            (6, 0),
            (2.7, 0),
            (2.7, 1.2),
            (1.2, 1.2),
            (1.2, 0),
            (1.2, 0.3),
            (2.7, 0.3),
            (2.7, 0.6),
            (1.2, 0.6),
            (1.2, 0.9),
            (2.7, 0.9),
            (2.7, 0)
        ]
            
    
    def update_positions(self, x, y):
        self.points =  [(dx+x, dy+y) for dx, dy in self.points]  

    def initialize_geometry(self):
        s1 = mpl_patches.Rectangle(
            self.points[0], 0.8, 0.8,
            color=self.color, ls=self.ls, fill=self.fill, lw=self.lw
        )
        s2 = mpl_patches.Rectangle(
            self.points[1], 0.8, 0.8,
            color=self.color, ls=self.ls, fill=self.fill, lw=self.lw
        )
        p = mpl_patches.Polygon(
            self.points[2:],
            color=self.color, ls=self.ls, fill=self.fill, lw=self.lw
        )
        return s1, s2, p

    def draw(self, ax):
        for p in self.initialize_geometry():
            ax.add_patch(p)
        return ax
```

## Dimensions and locations

```python
object_collection = dict(
    telek = Polygon([(0, 0), (14, 5), (14, 39), (0, 39)]),
    haz = Rectangle(6, 12),
    fenyo = Circle(2),
    mandula = Circle(1),
    terasz = CustomPlatform()
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
