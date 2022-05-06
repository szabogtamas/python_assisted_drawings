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

    def __init__(self, width, height, angle=0, color="k", ls="-", lw=0.1, fill=False, alpha=1):
        self.x = 0
        self.y = 0
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

    def initialize_geometry(self):
        p = mpl_patches.Rectangle(
            (self.x, self.y), self.w, self.h, angle=self.angle, color=self.color,
            ls=self.ls, lw=self.lw, fill=self.fill, alpha = self.alpha
        )
        return p

    def draw(self, ax):
        ax.add_patch(self.initialize_geometry())
        return ax

# Consider using something like https://lerner.co.il/2014/01/03/making-init-methods-magical-with-autoinit/ later
```

```python
class Ellipse(Rectangle):
# A primitive artist, an empty ellipse 

    def initialize_geometry(self):
        p = mpl_patches.Ellipse(
            (self.x, self.y), self.w, self.h, angle=self.angle, color=self.color,
            lw=self.lw, ls=self.ls, fill=self.fill, alpha = self.alpha
        )
        return p
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

```python
class Polygon(Rectangle):
# A primitive artist, a custom polygon

    def __init__(self, point_aray, color="k", ls="-", lw=0.1, fill=False, alpha=1):
        self.points_original = point_aray
        self.points = point_aray
        self.color = color
        self.ls = ls
        self.lw = lw
        self.fill = fill
        self.alpha = alpha 
    
    def update_positions(self, x, y):
        self.points =  [(dx+x, dy+y) for dx, dy in self.points_original]  

    def initialize_geometry(self):
        p = mpl_patches.Polygon(
            self.points, color=self.color, ls=self.ls, lw=self.lw,
            fill=self.fill, alpha = self.alpha
        )
        return p
```

```python
class CustomPlatform(Polygon):
# A composite object built up of multiple primitves

    def __init__(self, color="k", ls="-", lw=0.1, fill=False):
        self.color = color
        self.ls = ls
        self.lw = lw
        self.fill = fill
        self.points_original = [
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
        self.points = self.points_original
            
    
    def update_positions(self, x, y):
        self.points =  [(dx+x, dy+y) for dx, dy in self.points_original]  

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
    telek = Polygon([(0, 0), (14, 4), (14, 39), (0, 39)]),
    haz = Rectangle(6, 12),
    tornac = Rectangle(1, 7),
    lepcso = Polygon([(0, 0), (1, 0), (1, 2.8), (0, 2.8), (0, 2.5), (1, 2.5), (1, 2.2), (0, 2.2), (0, 1.9), (1, 1.9), (1, 0.9), (0, 0.9), (0, 0.6), (1, 0.6), (1, 0.3), (0, 0.3)]),
    terasz = CustomPlatform(),
    tarolo = Rectangle(2, 1.5),
    # pavilon = Rectangle(4, 5),
    pavilon = Polygon([(0, 1.5), (0, 4), (4, 4), (4, 0), (1.5, 0)]),
    pavilon2 = Polygon([(0, 0), (4, 0), (4, 1.5), (1.5, 1.5)], ls=":"),
    kocsi_elol = Rectangle(4, 5),
    kocsi_hatul = Polygon([(0, 0), (0, 5), (4, 5), (4, 1)]),
    platform1 = Rectangle(2, 2, color="red"),
    platform2 = Rectangle(2, 2, color="red"),
    magasagyas1 = Rectangle(1, 1),
    magasagyas2 = Rectangle(1, 1),
    magasagyas3 = Rectangle(1, 1),
    magasagyas4 = Rectangle(0.5, 2),
    diszagyas = Wedge(2, 90, -90),
    kisdisz = Circle(1),
    fenyo = Circle(1),
    mandula = Circle(1),
    gyumolcs1 = Circle(1),
    gyumolcs2 = Circle(1),
    gyumolcs3 = Circle(1),
    gyep = Ellipse(16, 8, angle=60),
    jatekos = Rectangle(1.5, 3, angle=60)
)
```

```python
object_locations = dict(
    telek = (0, 0),
    haz = (1, 24),
    tornac = (6, 29),
    lepcso = (7, 31),
    terasz = (1, 19),
    tarolo = (12, 34.5),
    pavilon = (10, 24),
    pavilon2 = (10, 28),
    kocsi_elol = (8, 34),
    kocsi_hatul = (10, 3),
    platform1 = (11, 10),
    platform2 = (11, 13),
    magasagyas1 = (13, 10),
    magasagyas2 = (13, 12),
    magasagyas3 = (13, 14),
    magasagyas4 = (0.5, 16),
    diszagyas = (14, 32.5),
    kisdisz = (12.5, 32.5),
    fenyo = (4, 37.5),
    mandula = (6, 12),
    gyep = (7, 12),
    jatekos = (3, 3),
    gyumolcs1 = (1.4, 2.1),
    gyumolcs2 = (4.4, 3.1),
    gyumolcs3 = (7.4, 4.1)
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
fig.savefig("terv1.pdf")
```

## Draw shadows

```python
shadow_collection = dict(
    haz_reggel = Polygon([(0, 6), (3, 0), (3, 10), (0, 12)], color="red", alpha=0.1, fill=True),
    haz_du = Polygon([(0, 0), (6, -3), (6, 9), (0, 12)], color="blue", alpha=0.1, fill=True),
    kerites_reggel = Polygon([(0, 0), (14, 4), (14, 5.5), (0, 1.5)], color="red", alpha=0.1, fill=True),
    kerites_du = Polygon([(0, 0), (1.5, 0.5), (1.5, 39), (0, 39)], color="blue", alpha=0.1, fill=True),
    mandula_reggel = Polygon([(0, 0), (0.5, 0), (3, 5), (5, 4)], color="red", alpha=0.1, fill=True),
    mandula_du = Polygon([(0, 0), (0.5, 0), (3, -6), (5, -6)], color="blue", alpha=0.1, fill=True)
)

shadow_locations = dict(
    haz_reggel = (11, 24),
    haz_du = (7, 24),
    kerites_reggel = (0, 0),
    kerites_du = (0, 0),
    mandula_reggel = (6, 12),
    mandula_du = (6, 12)
)
```

```python
for k, v in object_locations.items():
    object_collection[k].update_positions(*v)

for k, v in shadow_locations.items():
    shadow_collection[k].update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")

for k, v in object_collection.items():
    v.draw(ax)

for k, v in shadow_collection.items():
    v.draw(ax)
    
fig.savefig("arnyekok.pdf")
```

## Alernative plan

```python
object_locations = dict(
    magasagyas1 = (1.4, 2.1),
    magasagyas2 = (4.4, 3.1),
    magasagyas3 = (7.4, 4.1),
    magasagyas4 = (0.5, 4),
    jatekos = (2.5, 14),
    gyumolcs1 = (13, 12),
    gyumolcs2 = (13, 16),
    gyumolcs3 = (13, 20)
)

for k, v in object_locations.items():
    object_collection[k].update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")

for k, v in object_collection.items():
    v.draw(ax)

fig.savefig("alternativ_terv.pdf")
```

## Draw roads

```python
object_collection = dict(
    telek = Polygon([(0, 0), (14, 4), (14, 39), (0, 39)]),
    haz_elott = Rectangle(7, 12, color="blue", alpha=0.1, fill=True),
    haz = Rectangle(6, 12),
    tornac = Rectangle(1, 7),
    lepcso = Polygon([(0, 0), (1, 0), (1, 2.8), (0, 2.8), (0, 2.5), (1, 2.5), (1, 2.2), (0, 2.2), (0, 1.9), (1, 1.9), (1, 0.9), (0, 0.9), (0, 0.6), (1, 0.6), (1, 0.3), (0, 0.3)]),
    terasz = CustomPlatform(),
    tarolo = Rectangle(2, 1.5),
    pavilon = Polygon([(0, 1.5), (0, 4), (4, 4), (4, 0), (1.5, 0)]),
    pavilon2 = Polygon([(0, 0), (4, 0), (4, 1.5), (1.5, 1.5)], ls=":"),
    kocsi_elol = Rectangle(5, 3, color="blue", alpha=0.1, fill=True),
    kocsi_hatul = Polygon([(0, 0), (0, 5), (5.5, 5), (5.5, 1.3)], color="blue", alpha=0.1, fill=True),
    platform1 = Rectangle(2, 2, color="red"),
    platform2 = Rectangle(2, 2, color="red"),
    mandula = Circle(1),
    diszagyas = Wedge(2, 90, -90, color="white", fill=True),
    terasz_ut1 = Polygon([(0, 0), (0, 7), (5, 7)], color="blue", alpha=0.1, fill=True),
    terasz_ut2 = Polygon([(0, 0), (3, 0), (3, 5), (0, 5)], color="blue", alpha=0.1, fill=True),
    gyep_kint = Ellipse(21, 7, angle=55, color="blue", alpha=0.1, fill=True),
    gyep_bent = Ellipse(19, 5, angle=55, color="white", alpha=1, fill=True)
)

object_locations = dict(
    telek = (0, 0),
    haz = (1, 24),
    tornac = (6, 29),
    lepcso = (7, 31),
    terasz = (1, 19),
    tarolo = (12, 34.5),
    pavilon = (10, 24),
    pavilon2 = (10, 28),
    haz_elott = (7, 24),
    kocsi_elol = (7, 36),
    kocsi_hatul = (8.5, 2),
    platform1 = (11, 10),
    platform2 = (11, 13),
    mandula = (6, 12),
    diszagyas = (14, 32.5),
    terasz_ut1 = (2, 12),
    terasz_ut2 = (7, 19),
    gyep_kint = (7, 13),
    gyep_bent = (7, 13)
)

for k, v in object_locations.items():
    object_collection[k].update_positions(*v)

fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[-0.5, -0.5], color="white")

for k, v in object_collection.items():
    v.draw(ax)

fig.savefig("utak.pdf")
```

```python

```
