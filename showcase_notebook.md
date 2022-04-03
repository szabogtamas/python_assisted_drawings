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
from matplotlib.patches import Rectangle, Circle, Polygon
```

## Object definitions

```python
def draw_rectangle(x, y, w, h):
    r = Rectangle((x, y), w, h, fill=False)
    return r

def draw_circle(x, y, r):
    r = Circle((x, y), r, fill=False)
    return r
```

```python
def draw_balcony(x, y):
    dps = [
        (0, 0),
        (0, 5),
        (6, 5),
        (6, 0),
        (2.8, 0),
        (2.8, 0.9),
        (1.3, 0.9),
        (1.3, 0)
    ]
    r = Polygon([(dx+x, dy+y) for dx, dy in dps], fill=False)
    return r
```

## Dimensions and locations

```python
object_collection = dict(
    telek = [draw_rectangle, 0, 0, 12, 36],
    haz = [draw_rectangle, 0, 0, 6, 12],
    terasz = [draw_balcony, 0, 0],
    fa = [draw_circle, 0, 0, 2]
)
```

```python
object_locations = dict(
    telek = (0, 0),
    haz = (1, 20),
    terasz = (1, 15),
    fa = (6, 8)
)
```

## Draw plan

```python
for k, v in object_locations.items():
    object_collection[k][1:3] = v
```

```python
fig, ax = plt.subplots(figsize=(2, 6))

ax.set_aspect("equal", adjustable="datalim")
ax.axis('off')
ax.plot([0, 12],[0, 0], color="white")

for k, v in object_collection.items():
    ax.add_patch(v[0](*v[1:]))
```

```python
fig.savefig("plan_example.pdf")
```
