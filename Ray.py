from vpython import *
import numpy as np

dt = 0.001

nair = 1.0
nwater = [1.3320, 1.3325, 1.3331, 1.3349, 1.3390, 1.3435]


class Ray:
    def __init__(self, _pos=vec(0, 0, 0), angle=0):
        self.pos = []
        self.v = []

        self.in_lens = [False, False, False, False, False, False]
        self.reflected = [0, 0, 0, 0, 0, 0]

        for i in range(6):
            self.v.append(vec(cos(-angle), sin(-angle), 0))
            self.pos.append(_pos)

        self.white = sphere(
            pos=_pos,
            color=color.white,
            radius=0.01,
            make_trail=True,
            v=vec(cos(-angle), sin(-angle), 0)
        )

        ray_radius = 0.0001
        self.rays = [
            sphere(pos=_pos, color=color.red,
                   radius=ray_radius, make_trail=False),
            sphere(pos=_pos, color=color.orange,
                   radius=ray_radius, make_trail=False),
            sphere(pos=_pos, color=color.yellow,
                   radius=ray_radius, make_trail=False),
            sphere(pos=_pos, color=color.green,
                   radius=ray_radius, make_trail=False),
            sphere(pos=_pos, color=color.blue,
                   radius=ray_radius, make_trail=False),
            sphere(pos=_pos, color=color.purple,
                   radius=ray_radius, make_trail=False)
        ]

    # does refract if there is one
    # param type = 'in' or 'out'
    def refract(self, droplet_pos, droplet_r):
        for i in range(6):
            if not self.in_lens[i] and self.reflected[i] == 0 and mag(droplet_pos - self.pos[i]) <= droplet_r:
                type = 'in'
                self.white.v = vec(0, 0, 0)
                self.rays[i].make_trail = True
                self.rays[i].visible = True
                self.in_lens[i] = True
            elif self.in_lens[i] and self.reflected[i] >= 1 and mag(droplet_pos - self.pos[i]) >= droplet_r:
                type = 'out'
                self.in_lens[i] = False
            else:
                continue
            n1 = nair if type == 'in' else nwater[i]
            n2 = nair if type == 'out' else nwater[i]
            normal_v = norm(droplet_pos - self.pos[i])
            normal_v *= -1 if type == 'out' else 1
            angle_out = asin(n1 / n2 * sin(diff_angle(self.v[i], normal_v)))
            self.v[i] = rotate(
                normal_v,
                angle=angle_out,
                axis=cross(normal_v, self.v[i])
            )
            # print('refract!', i, self.pos[i])
            self._update()

    def reflect(self, droplet_pos, droplet_r):
        for i in range(6):
            if self.in_lens[i] and self.reflected[i] == 0 and mag(droplet_pos - self.pos[i]) >= droplet_r:
                self.reflected[i] += 1
                normal_v = norm(droplet_pos - self.pos[i])
                angle_out = diff_angle(-self.v[i], normal_v)
                self.v[i] = rotate(normal_v, angle=angle_out,
                                   axis=cross(normal_v, self.v[i]))
                self._update()

    def _update(self):
        for i in range(6):
            self.pos[i] += self.v[i] * dt
            self.rays[i].pos = self.pos[i]

    def update(self, droplet_pos, droplet_r):
        for i in range(6):
            self.refract(droplet_pos, droplet_r)
            self.reflect(droplet_pos, droplet_r)
            self.pos[i] += self.v[i] * dt
            self.rays[i].pos = self.pos[i]
        self.white.pos += self.white.v * dt


def run(slider):
    angle = slider.value
    for position in range(3, 9):
        ray = Ray(rotate(vec(-4, position/5, 0), -angle), 0)
        done = False
        while not done:
            rate(10000)
            ray.update(droplet.pos, droplet.radius)

            for i in range(6):
                if mag(ray.pos[i]) >= 5:
                    print(i, ray.pos[i].y)
                    done = True
                    break


scene = canvas(background=vec(0.5, 0.5, 0.5), width=1200,
               height=600, center=vec(0, 0, 0))

bg = box(pos=vec(0, 0, 0), size=vec(
    20, 10, 0.0001), color=vec(0.2, 0.5, 0.5))

angle_slider = slider(vertical=True, max=pi/2, value=0,
                      bind=run, align='left', pos=scene.title_anchor)

# droplet radius
r = 2
droplet = sphere(
    radius=r,
    pos=vec(0, 0, 0),
    color=vec(195/255, 253/255, 255/255),
    opacity=0.2
)

dropletCenter = sphere(radius=0.05, pos=droplet.pos, color=color.red)
