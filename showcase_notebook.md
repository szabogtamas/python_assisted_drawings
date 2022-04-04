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
```

## Define artist objects

```python
class Rectangle:
# A most basic artist, a rectangle that will also be building block of other objects

    def __init__(self, width, height, color="k", ls="-", fill=False):
        self.x = 0
        self.y = 0
        self.w = width
        self.h = height
        self.color = color
        self.ls = ls
        self.fill = fill
    
    def update_positions(self, x, y):
        self.x = x
        self.y = y

    def initialize_geometry(self):
        p = mpl_patches.Rectangle(
            (self.x, self.y), self.w, self.h,
            color=self.color, ls=self.ls, fill=self.fill
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

    def __init__(self, r, color="k", ls="-", fill=False):
        self.x = 0
        self.y = 0
        self.r = r
        self.color = color
        self.ls = ls
        self.fill = fill        

    def initialize_geometry(self):
        p = mpl_patches.Circle(
            (self.x, self.y), self.r,
            color=self.color, ls=self.ls, fill=self.fill
        )
        return p
```

```python
class Polygon(Rectangle):
# A primitive artist, a custom polygon

    def __init__(self, point_aray, color="k", ls="-", fill=False):
        self.points = point_aray
        self.color = color
        self.ls = ls
        self.fill = fill
    
    def update_positions(self, x, y):
        self.points =  [(dx+x, dy+y) for dx, dy in self.points]  

    def initialize_geometry(self):
        p = mpl_patches.Polygon(
            self.points,
            color=self.color, ls=self.ls, fill=self.fill
        )
        return p
```

## Dimensions and locations

```python
object_collection = dict(
    telek = Polygon([(0, 0), (12, 6), (12, 41), (0, 41)]),
    haz = Rectangle(6, 12),
    fa = Circle(2)
)
```

```python
object_locations = dict(
    telek = (0, 0),
    haz = (1, 25),
    fa = (6, 12)
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
