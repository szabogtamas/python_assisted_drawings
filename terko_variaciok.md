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
!pip3 install pysolar
!pip install shapely
```

```python
from pysolar import solar
from shapely import geometry as sg
import datetime
import math
import numpy as np
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
        
    def update_positions(self, x, y):
        self.x = x
        self.y = y
    
    def rotate_edge(self, points, origin, angle):
        points = complex(*points)
        origin = complex(*origin)
        angle = np.deg2rad(angle)
        r = (points - origin) * np.exp(complex(0, angle)) + origin
        return (r.real, r.imag)
    
    def initialize_geometry(self):
        p = mpl_patches.Rectangle(
            (self.x, self.y), self.w, self.h, angle=self.angle, color=self.color,
            ls=self.ls, lw=self.lw, fill=self.fill, alpha = self.alpha
        )
        return p

    def draw(self, ax):
        ax.add_patch(self.initialize_geometry())
        return ax

    def draw_shadowed(self, ax):
        for p in self.initialize_shadow():
            ax.add_patch(p)
        if not self.shadow_only:
            ax.add_patch(self.initialize_geometry())
        return ax
```

```python
class Polygon(Rectangle):
# A primitive artist, a custom polygon

    def __init__(
        self, point_aray, color="k", ls="-", lw=0.2,
        fill=False, alpha=1, z=2, sun_h=None, sun_a=None, sun_r=None,
        shadow_color="#D3D3D3", shadow_only=False
    ):
        self.points_original = point_aray
        self.points = point_aray
        self.z = z
        self.color = color
        self.ls = ls
        self.lw = lw
        self.fill = fill
        self.alpha = alpha
    
    def update_positions(self, x, y):
        self.points =  [(dx+x, dy+y) for dx, dy in self.points_original]  
    
    def area(self):
        return sg.Polygon(self.points).area

    def initialize_geometry(self):
        p = mpl_patches.Polygon(
            self.points, color=self.color, ls=self.ls, lw=self.lw,
            fill=self.fill, alpha = self.alpha
        )
        return p
```

```python
class Wedge(Rectangle):
# A primitive artist, a half circle

    def __init__(self, r, t1=0, t2=180, color="k", ls="-", lw=0.1, fill=False):
        self.x = 0
        self.y = 0
        self.r = r
        self.t1 = t1
        self.t2 = t2
        self.color = color
        self.ls = ls
        self.lw = lw
        self.fill = fill        

    def initialize_geometry(self):
        p = mpl_patches.Wedge(
            (self.x, self.y), self.r, self.t1, self.t2,
            color=self.color, ls=self.ls, fill=self.fill, lw=self.lw
        )
        return p
```

## Initial plan

```python
terko_pontok = [
    (190, 0), (190, 480), (0, 480), (0, 830), (190, 830), (190, 1370),
    (0, 1370), (0, 1650), (540, 1650), (540, 1870),
    (540, 2380), (300, 2380), (240, 2380), (240, 2440), (300, 2440),
    (300, 3820), (240, 3820), (240, 4000), (360, 4000), (360, 2500), 
    (660, 2500), (1000, 2500), (1000, 2560), (1150, 2560), (1150, 2500),
    (1300, 2500), (1300, 2350), (690, 2350), (690, 1870),
    (610, 1870), (610, 1650), (610, 1370), (510, 1370), (510, 1120),
    (510, 830), (610, 830), (610, 480), (720, 480), (720, 0)
]

object_collection = dict(
    terko = Polygon(terko_pontok)
)

object_locations = dict(
    terko = (0, 0)
)

terulet = object_collection["terko"].area() / 10000

for k, v in object_locations.items():
    object_collection[k].update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")
ax.set_title(str(terulet) + "m2")

for k, v in object_collection.items():
    v.draw(ax)

#fig.savefig("tervek/terko_terv.pdf")
```

```python
terko_pontok = [
    (190, 0), (190, 480), (0, 480), (0, 830), (190, 830), (190, 1370),
    (0, 1370), (0, 1650), (480, 1650), (480, 1870),
    (480, 2380), (300, 2380), (240, 2380), (240, 2440), (300, 2440),
    (300, 3820), (240, 3820), (240, 4000), (360, 4000), (360, 2500), 
    (660, 2500), (1000, 2500), (1000, 2560), (1150, 2560), (1150, 2500),
    (1300, 2500), (1300, 2350), (690, 2350), (690, 1870),
    (610, 1870), (610, 1650), (610, 1370), (510, 1370), (510, 1120),
    (510, 830), (610, 830), (610, 480), (720, 480), (720, 0)
]

object_collection = dict(
    terko = Polygon(terko_pontok)
)

object_locations = dict(
    terko = (0, 0)
)

terulet = object_collection["terko"].area() / 10000

for k, v in object_locations.items():
    object_collection[k].update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")
ax.set_title(str(terulet) + "m2")

for k, v in object_collection.items():
    v.draw(ax)
```

```python
terko_pontok = [
    (190, 0), (190, 480), (190, 480), (190, 830), (190, 830), (190, 1370),
    (0, 1370), (0, 1650), (480, 1650), (480, 1870),
    (480, 2380), (300, 2380), (240, 2380), (240, 2440), (300, 2440),
    (300, 3820), (240, 3820), (240, 4000), (360, 4000), (360, 2500), 
    (660, 2500), (1000, 2500), (1000, 2560), (1150, 2560), (1150, 2500),
    (1300, 2500), (1300, 2350), (690, 2350), (690, 1870),
    (610, 1870), (610, 1650), (610, 1370), (510, 1370), (510, 1120),
    (510, 830), (610, 830), (610, 480), (720, 480), (720, 0)
]

object_collection = dict(
    terko = Polygon(terko_pontok, color="grey", fill=True)
)

object_locations = dict(
    terko = (0, 0)
)

terulet = object_collection["terko"].area() / 10000

for k, v in object_locations.items():
    object_collection[k].update_positions(*v)

fig, ax = plt.subplots(figsize=(7.2, 9.6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")
ax.set_title(str(terulet) + "m2\n06 70 704 8910")

for k, v in object_collection.items():
    v.draw(ax)

fig.savefig("tervek/terko_terv_a4.pdf")
```

```python
terko_pontok = [
    (190, 0), (190, 480), (0, 480), (0, 830), (190, 830), (190, 1370),
    (0, 1370), (0, 1650), (480, 1650), (480, 1870), (540, 1930), (540, 2320),
    (480, 2380), (360, 2380), (300, 2440), (300, 3820), (240, 3820),
    (240, 4000), (360, 4000), (360, 2560), (420, 2500), 
    (660, 2500), (1000, 2500), (1000, 2560), (1150, 2560), (1150, 2500),
    (1300, 2500), (1300, 2350), (690, 2350), (690, 1870),
    (610, 1870), (610, 1650), (610, 1370), (510, 1370), (510, 1120),
    (510, 830), (610, 830), (610, 480), (720, 480), (720, 0)
]

object_collection = dict(
    terko = Polygon(terko_pontok)
)

object_locations = dict(
    terko = (0, 0)
)

terulet = object_collection["terko"].area() / 10000

for k, v in object_locations.items():
    object_collection[k].update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")
ax.set_title(str(terulet) + "m2")

for k, v in object_collection.items():
    v.draw(ax)
```

```python
terko_pontok = [
    (190, 0), (190, 480), (0, 480), (0, 830), (190, 830), (190, 1370),
    (0, 1370), (0, 1650), (480, 1650), (480, 1870),
    (480, 2380), (300, 2380), (240, 2380), (240, 2440), (300, 2440),
    (300, 3820), (240, 3820), (240, 4000), (360, 4000), (360, 2500), 
    (660, 2500), (1000, 2500), (1000, 2560), (1150, 2560), (1150, 2500),
    (1300, 2500), (1300, 2350), (690, 2350), (690, 1870),
    (610, 1870), (610, 1650), (610, 1370), (510, 1370), (510, 1120),
    (510, 830), (610, 830), (610, 480), (720, 480), (720, 0)
]

object_collection = dict(
    terko = Polygon(terko_pontok),
    w0 = Wedge(300, 90, 180, color="red", lw=0.5),
    w1 = Wedge(300, 0, 90, color="grey", fill=True),
    w2 = Wedge(500, -90, 0, color="grey", fill=True),
    w3 = Wedge(200, 90, 180, color="grey", fill=True),
    w4 = Wedge(200, 180, -90, color="red", lw=0.5)
)

object_locations = dict(
    terko = (0, 0),
    w0 = (800, 2150),
    w1 = (200, 2150),
    w2 = (0, 2150),
    w3 = (200, 2250),
    w4 = (200, 2650)
)

terulet = object_collection["terko"].area() / 10000

for k, v in object_locations.items():
    object_collection[k].update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")
ax.set_title(str(terulet) + "m2")

for k, v in object_collection.items():
    v.draw(ax)

fig.savefig("tervek/terko_terv.pdf")
```

```python
terko_pontok = [
    (190, 0), (190, 480), (0, 480), (0, 830), (190, 830), (190, 1370),
    (0, 1370), (0, 1650), (480, 1650), (480, 1870),
    (480, 2380), (300, 2380), (240, 2380), (240, 2440), (300, 2440),
    (300, 3820), (240, 3820), (240, 4000), (360, 4000), (360, 2500), 
    (660, 2500), (1000, 2500), (1000, 2560), (1150, 2560), (1150, 2500),
    (1300, 2500), (1300, 2350), (690, 2350), (690, 1870),
    (610, 1870), (610, 1650), (610, 1370), (510, 1370), (510, 1120),
    (510, 830), (610, 830), (610, 480), (720, 480), (720, 0)
]

object_collection = [
    (Wedge(590, -90, 0, color="grey", fill=True), (0, 2150)),
    (Wedge(500, -90, 0, color="green", fill=True), (0, 2150)),
    (Wedge(390, 0, 90, color="grey", fill=True), (200, 2150)),
    (Wedge(300, 0, 90, color="green", fill=True), (200, 2150)),
    (Wedge(290, 90, 180, color="grey", fill=True), (200, 2250)),
    (Wedge(200, 90, 180, color="green", fill=True), (200, 2250)),
    (Wedge(100, 180, -90, color="green", fill=True), (100, 2250)),
    (Wedge(390, 90, 180, color="grey", fill=True), (900, 2150)),
    (Wedge(300, 90, 180, color="white", fill=True), (900, 2150)),
    (Wedge(290, -90, 0, color="grey", fill=True), (900, 2750)),
    (Wedge(200, -90, 0, color="white", fill=True), (900, 2750)),
    (Wedge(190, 0, 90, color="grey", fill=True), (1000, 2750)),
    (Wedge(100, 0, 90, color="white", fill=True), (1000, 2750)),
    (Wedge(290, 180, -90, color="grey", fill=True), (200, 2750)),
    (Wedge(200, 180, -90, color="white", fill=True), (200, 2750)),
    (Wedge(190, 90, 180, color="grey", fill=True), (100, 2750)),
    (Wedge(100, 90, 180, color="white", fill=True), (100, 2750)),
    (Polygon(terko_pontok), (0, 0))
]

terulet = object_collection[-1][0].area() / 10000

for k, v in object_collection:
    k.update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")
ax.set_title(str(terulet) + "m2")

for k, v in object_collection:
    k.draw(ax)

#fig.savefig("tervek/terko_terv.pdf")
```

```python
terko_pontok = [
    (190, 0), (190, 480), (0, 480), (0, 830), (190, 830), (190, 1370),
    (0, 1370), (0, 1650), (480, 1650), (480, 1870),
    (480, 2380), (300, 2380), (240, 2380), (240, 2440), (300, 2440),
    (300, 3820), (240, 3820), (240, 4000), (360, 4000), (360, 2500), 
    (660, 2500), (1000, 2500), (1000, 2560), (1150, 2560), (1150, 2500),
    (1300, 2500), (1300, 2350), (690, 2350), (690, 1870),
    (610, 1870), (610, 1650), (610, 1370), (510, 1370), (510, 1120),
    (510, 830), (610, 830), (610, 480), (720, 480), (720, 0)
]

object_collection = [
    (Wedge(590, -90, 0, color="grey", fill=True), (0, 2150)),
    (Wedge(500, -90, 0, color="green", fill=True), (0, 2150)),
    (Wedge(390, 0, 90, color="grey", fill=True), (0, 1200)),
    (Wedge(300, 0, 90, color="white", fill=True), (0, 1200)),
    (Wedge(390, 0, 90, color="grey", fill=True), (200, 2150)),
    (Wedge(300, 0, 90, color="green", fill=True), (200, 2150)),
    (Wedge(290, 90, 180, color="grey", fill=True), (200, 2250)),
    (Wedge(200, 90, 180, color="green", fill=True), (200, 2250)),
    (Wedge(100, 180, -90, color="green", fill=True), (100, 2250)),
    (Wedge(190, -90, 0, color="grey", fill=True), (200, 2650)),
    (Wedge(100, -90, 0, color="white", fill=True), (200, 2650)),
    (Wedge(390, 90, 180, color="grey", fill=True), (900, 2150)),
    (Wedge(300, 90, 180, color="white", fill=True), (900, 2150)),
    (Wedge(290, -90, 0, color="grey", fill=True), (900, 2750)),
    (Wedge(200, -90, 0, color="white", fill=True), (900, 2750)),
    (Wedge(190, 0, 90, color="grey", fill=True), (1000, 2750)),
    (Wedge(100, 0, 90, color="white", fill=True), (1000, 2750)),
    (Wedge(290, 180, -90, color="grey", fill=True), (200, 2750)),
    (Wedge(200, 180, -90, color="white", fill=True), (200, 2750)),
    (Wedge(190, 90, 180, color="grey", fill=True), (100, 2750)),
    (Wedge(100, 90, 180, color="white", fill=True), (100, 2750)),
    (Polygon(terko_pontok), (0, 0))
]

terulet = object_collection[-1][0].area() / 10000

for k, v in object_collection:
    k.update_positions(*v)

fig, ax = plt.subplots(figsize=(7.2, 9.6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")
ax.set_title(str(terulet) + "m2")

for k, v in object_collection:
    k.draw(ax)

fig.savefig("tervek/terko_spiral_terv.pdf")
```

```python
terko_pontok = [
    (190, 0), (190, 480), (0, 480), (0, 830), (190, 830), (190, 1370),
    (0, 1370), (0, 1650), (480, 1650), (480, 1870),
    (480, 2380), (300, 2380), (240, 2380), (240, 2440), (300, 2440),
    (300, 3820), (240, 3820), (240, 4000), (360, 4000), (360, 2500), 
    (660, 2500), (1000, 2500), (1000, 2560), (1150, 2560), (1150, 2500),
    (1300, 2500), (1300, 2350), (690, 2350), (690, 1870),
    (610, 1870), (610, 1650), (610, 1370), (510, 1370), (510, 1120),
    (510, 830), (610, 830), (610, 480), (720, 480), (720, 0)
]

object_collection = [
    (Wedge(270, -90, 0, color="grey", fill=True), (290, 2150)),
    (Wedge(210, -90, 0, color="green", fill=True), (290, 2150)),
    (Wedge(400, 0, 90, color="grey", fill=True), (0, 1200)),
    (Wedge(340, 0, 90, color="green", fill=True), (0, 1200)),
    (Wedge(400, 0, 90, color="grey", fill=True), (200, 2150)),
    (Wedge(340, 0, 90, color="green", fill=True), (200, 2150)),
    (Wedge(290, 90, 180, color="grey", fill=True), (200, 2250)),
    (Wedge(200, 90, 180, color="green", fill=True), (200, 2250)),
    (Wedge(100, 180, -90, color="green", fill=True), (100, 2250)),
    (Wedge(400, 90, 180, color="grey", fill=True), (900, 2150)),
    (Wedge(340, 90, 180, color="white", fill=True), (900, 2150)),
    (Wedge(290, -90, 0, color="grey", fill=True), (900, 2750)),
    (Wedge(200, -90, 0, color="white", fill=True), (900, 2750)),
    (Wedge(190, 0, 90, color="grey", fill=True), (1000, 2750)),
    (Wedge(100, 0, 90, color="white", fill=True), (1000, 2750)),
    (Wedge(290, 180, -90, color="grey", fill=True), (200, 2750)),
    (Wedge(200, 180, -90, color="white", fill=True), (200, 2750)),
    (Wedge(190, 90, 180, color="grey", fill=True), (100, 2750)),
    (Wedge(100, 90, 180, color="white", fill=True), (100, 2750)),
    (Polygon(terko_pontok), (0, 0))
]

terulet = object_collection[-1][0].area() / 10000

for k, v in object_collection:
    k.update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")
ax.set_title(str(terulet) + "m2")

for k, v in object_collection:
    k.draw(ax)

#fig.savefig("tervek/terko_terv.pdf")
```

```python
terko_pontok = [
    (190, 0), (190, 480), (0, 480), (0, 830), (190, 830), (190, 1370),
    (0, 1370), (0, 1650), (480, 1650), (480, 1870),
    (610, 1870), (610, 1650), (610, 1370), (510, 1370), (510, 1120),
    (510, 830), (610, 830), (610, 480), (720, 480), (720, 0)
]

object_collection = [
    (Polygon(terko_pontok), (0, 0))
]

terulet = object_collection[-1][0].area() / 10000

for k, v in object_collection:
    k.update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")
ax.set_title(str(terulet) + "m2")

for k, v in object_collection:
    k.draw(ax)

#fig.savefig("tervek/terko_terv.pdf")
```

```python
terko_pontok = [
    (190, 0), (190, 480), (0, 480), (0, 830), (190, 830), (190, 1370),
    (0, 1370), (0, 1650), (480, 1650), (480, 1870),
    (480, 2380), (300, 2380), (240, 2380), (240, 2440), (300, 2440),
    (300, 3820), (240, 3820), (240, 4000), (360, 4000), (360, 2500), 
    (660, 2500), (1000, 2500), (1000, 2560), (1150, 2560), (1150, 2500),
    (1300, 2500), (1300, 2350), (690, 2350), (690, 1870),
    (610, 1870), (610, 1650), (610, 1370), (510, 1370), (510, 1120),
    (510, 830), (610, 830), (610, 480), (720, 480), (720, 0)
]

object_collection = [(Wedge(270, -90, 0, color="grey", fill=True), (290, 2150)),
    (Wedge(210, -90, 0, color="green", fill=True), (290, 2150)),
    (Wedge(400, 0, 90, color="grey", fill=True), (200, 2150)),
    (Wedge(340, 0, 90, color="green", fill=True), (200, 2150)),
    (Wedge(290, 90, 180, color="grey", fill=True), (200, 2250)),
    (Wedge(200, 90, 180, color="green", fill=True), (200, 2250)),
    (Wedge(100, 180, -90, color="green", fill=True), (100, 2250)),
    
    (Wedge(144, 0, 45, color="grey", fill=True), (160, 2590)),
    (Wedge(84, 0, 45, color="white", fill=True), (160, 2590)),
    (Wedge(89, 45, 90, color="grey", fill=True), (160, 2590)),
    (Wedge(29, 45, 90, color="green", fill=True), (160, 2590)),
    (Wedge(89, -135, -90, color="grey", fill=True), (160, 2705)),
    (Wedge(29, -135, -90, color="white", fill=True), (160, 2705)),
    (Wedge(144, 180, -135, color="grey", fill=True), (200, 2750)),
    (Wedge(84, 180, -135, color="white", fill=True), (200, 2750))#,
    #(Polygon(terko_pontok), (0, 0))
]

terulet = "" # object_collection[-1][0].area() / 10000

for k, v in object_collection:
    k.update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 1],[-0.5, -0.5], color="white")
ax.set_title(str(terulet) + "m2")

for k, v in object_collection:
    k.draw(ax)

#fig.savefig("tervek/terko_terv.pdf")
```

```python
fib(1, 15)
```

## Fibonacci spiralok

```python
def initialize_fib(n):
    c, d = 0, True
    a, b = 0, 1
    while c < 20 and d:
        c += 1
        a1 = a + 0
        a  = b + 0
        b = a1 + b
        if b >= n:
            d = False
    return a, b

def fib(start, length):
    a, b = initialize_fib(start)
    l = []
    for i in range(0, length):
        a1 = a + 0
        a  = b + 0
        b = a1 + b
        l.append(a)
        
    return(l)

def rotate_edge(points, origin, angle):
        points = complex(*points)
        origin = complex(*origin)
        angle = np.deg2rad(angle)
        r = (points - origin) * np.exp(complex(0, angle)) + origin
        return (r.real, r.imag)

def draw_fibonacci_spiral(start, N, angle=90, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(3.6, 4.8))
    
    origin = np.array([0, 0])
    xy = np.array([0, 0])
    a1 = 0
    a2 = a1 + angle
    fs = fib(start, N)
    for i, n in enumerate(fs[::-1]):
        f2 = fs[N-i-2]
        p = mpl_patches.Wedge(xy, n, a1, a2, color="grey", fill=True, alpha=0.3)
        ax.add_patch(p)
        a1 = a1 + angle
        a2 = a2 + angle
        slide_vector = rotate_edge((n -f2, 0), origin, a1)
        xy = xy + slide_vector
    
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis('off')
    ax.plot([0, 12],[-0.5, -0.5], color="white")
    
    return ax
```

```python
fib(1, 15)
```

```python
draw_fibonacci_spiral(3, 7, 90)
```

```python
fig, axs = plt.subplots(3, 2, figsize=(7.2, 9.6))
axs = axs.flatten()

experimental_axes = [15, 30, 45, 60, 90, 120]

for i, e in enumerate(experimental_axes):
    axs[i] = draw_fibonacci_spiral(1, 20, e, ax=axs[i])

fig.savefig("fibonacci_spiral_szogek.pdf")
```

```python
fig, axs = plt.subplots(3, 2, figsize=(7.2, 9.6))
axs = axs.flatten()

experimental_axes = [10, 15, 30, 60, 90, 120]

for i, e in enumerate(experimental_axes):
    axs[i] = draw_fibonacci_spiral(1, 20, e, ax=axs[i])

fig.savefig("fibonacci_spiral_szogek.pdf")
```

```python
start = 20
N = 4
angle = 60

fig, ax = plt.subplots(figsize=(3.6, 4.8))
    
origin = np.array([0, 0])
xy = np.array([0, 0])
a1 = 0
a2 = a1 + angle
fs = fib(start, N)
for i, n in enumerate(fs[N-2::-1]):
    f2 = fs[N-i-3]
    p = mpl_patches.Wedge(xy, n, a1, a2, color="grey", fill=True, alpha=0.3)
    ax.add_patch(p)
    a1 = a1 + angle
    a2 = a2 + angle
    slide_vector = rotate_edge((n - f2, 0), origin, a1)
    xy = xy + slide_vector

a1 = a1 + 180 - angle
a2 = a2 + 180 - angle
#xy = np.array([0, 0])
last_stand = n + 0
xy = xy - slide_vector - np.array([2*last_stand, 0])
for i, n in enumerate(fs[:-1]):
    f2 = fs[i+1]
    p = mpl_patches.Wedge(xy, n, a1, a2, color="grey", fill=True, alpha=0.3)
    ax.add_patch(p)
    a1 = a1 - angle
    a2 = a2 - angle
    slide_vector = rotate_edge((n - f2, 0), origin, a2)
    xy = xy + slide_vector # + np.array([last_stand, 0])

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")
```

```python
def draw_fibonacci_stripe(start, N, width, angle=90, start_angle=0, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(3.6, 4.8))
    
    origin = np.array([0, 0])
    xy = np.array([0, 0])
    fs = fib(start, N)
    for i, n in enumerate(fs[::-1]):
        f2 = fs[N-i-2]
        a2 = start_angle + angle
        p = mpl_patches.Wedge(xy, n, start_angle, a2, color="grey", fill=True, alpha=0.3)
        #p = mpl_patches.Wedge(xy*-1, n, start_angle, a2, color="grey", fill=True, alpha=0.3)
        ax.add_patch(p)
        #p = mpl_patches.Wedge(xy*-1, n-width, start_angle, a2, color="white", fill=True, alpha=1)
        p = mpl_patches.Wedge(xy, n-width, start_angle, a2, color="white", fill=True, alpha=1)
        ax.add_patch(p)
        start_angle = start_angle + angle
        slide_vector = rotate_edge((n -f2, 0), origin, start_angle)
        xy = xy + slide_vector
    
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis('off')
    ax.plot([0, 12],[-0.5, -0.5], color="white")
    return ax

fig, zax = plt.subplots(figsize=(7.2, 9.6))

zax.add_patch(mpl_patches.Rectangle((12.8, -18.8), 5.8, 7.6, color="grey", fill=True, alpha=0.3))
draw_fibonacci_stripe(3, 6, 2, angle=45, start_angle=225, ax=zax)
zax.add_patch(mpl_patches.Rectangle((6.4, -13.4), 6, 7.6, color="grey", fill=True, alpha=0.3))
zax.add_patch(mpl_patches.Wedge((12.7, -8.2), 5, -135, -90, color="red", fill=True, alpha=0.3))
zax.add_patch(mpl_patches.Wedge((12.7, -8.2), 3, -135, -90, color="white", fill=True, alpha=1))
zax.add_patch(mpl_patches.Wedge((14.8, -5.9), 8, -180, -135, color="red", fill=True, alpha=0.3))
zax.add_patch(mpl_patches.Wedge((14.8, -5.9), 6, -180, -135, color="white", fill=True, alpha=1))
```

```python
fig, axs = plt.subplots(3, 2, figsize=(7.2, 9.6))
axs = axs.flatten()

experimental_axes = [10, 15, 30, 60, 90, 120]

for i, e in enumerate(experimental_axes):
    axs[i] = draw_fibonacci_stripe(5, 7, 3, e, ax=axs[i])

fig.savefig("fibonacci_szalag_szogek.pdf")
```

```python

```
