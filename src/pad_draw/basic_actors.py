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

    def initialize_shadow(self):
        p1 = mpl_patches.Polygon(
            [
                (self.x, self.y+self.h),
                (self.x+self.w, self.y+self.h),
                self.rotate_edge((self.x+self.w, self.y+self.h+self.sun_tn), (self.x+self.w, self.y+self.h), self.sun_a),
                self.rotate_edge((self.x, self.y+self.h+self.sun_tn), (self.x, self.y+self.h), self.sun_a)
            ],
            color=self.shadow_color, fill=True, alpha=0.1
        )
        p2 = mpl_patches.Polygon(
            [
                (self.x+self.w, self.y+self.h),
                (self.x+self.w, self.y),
                self.rotate_edge((self.x+self.w, self.y+self.sun_tn), (self.x+self.w, self.y), self.sun_a),
                self.rotate_edge((self.x+self.w, self.y+self.h+self.sun_tn), (self.x+self.w, self.y+self.h), self.sun_a)
            ],
            color=self.shadow_color, fill=True, alpha=0.1
        )
        p3 = mpl_patches.Polygon(
            [
                (self.x+self.w, self.y),
                (self.x, self.y),
                self.rotate_edge((self.x, self.y+self.sun_tn), (self.x, self.y), self.sun_a),
                self.rotate_edge((self.x+self.w, self.y+self.sun_tn), (self.x+self.w, self.y), self.sun_a)
            ],
            color=self.shadow_color, fill=True, alpha=0.1
        )
        p4 = mpl_patches.Polygon(
            [
                (self.x, self.y+self.h),
                (self.x, self.y),
                self.rotate_edge((self.x, self.y+self.sun_tn), (self.x, self.y), self.sun_a),
                self.rotate_edge((self.x, self.y+self.h+self.sun_tn), (self.x, self.y+self.h), self.sun_a)
            ],
            color=self.shadow_color, fill=True, alpha=0.1
        )
        return p1, p2, p3, p4

    def draw(self, ax):
        ax.add_patch(self.initialize_geometry())
        return ax

    def draw_shadowed(self, ax):
        for p in self.initialize_shadow():
            ax.add_patch(p)
        if not self.shadow_only:
            ax.add_patch(self.initialize_geometry())
        return ax