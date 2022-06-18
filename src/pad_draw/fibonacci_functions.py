from matplotlib import pylab as plt
from matplotlib import patches as mpl_patches

def initialize_fib(n, cycle_limit=100):
    # Return the previous Fibonacci number (only if it is smaller than than first few given by cycle_limit)
    c, d = 0, True
    a, b = 0, 1
    while c < cycle_limit and d:
        c += 1
        a1 = a + 0
        a  = b + 0
        b = a1 + b
        if b >= n:
            d = False
    return a, b

def generate_fibonacci_series(start, length):
    # Return a series of Fibonacci numbers starting from a given number
    a, b = initialize_fib(start)
    l = []
    for i in range(0, length):
        a1 = a + 0
        a  = b + 0
        b = a1 + b
        l.append(a)

    return(l)

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
