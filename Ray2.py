from vpython import *
import numpy as np

nair = 1.0
nwater = [1.3320, 1.3325, 1.3331, 1.3349, 1.3390, 1.3435]


class Ray:
    def __init__(self, _pos=vec(0, 0, 0), angle=0):
        self.pos = np.array([], dtype=vec)
        self.v = np.array([], dtype=vec)
        self.log = [[], [], [], [], [], []]
        self.dt = 0.001

        self.in_lens = [False, False, False, False, False, False]
        self.reflected = [0, 0, 0, 0, 0, 0]

        for i in range(6):
            self.v = np.append(self.v, vec(cos(-angle), sin(-angle), 0))
            self.pos = np.append(self.pos, _pos)

        beam_radius = 0.01
        self.white = cylinder(
            pos=_pos,
            color=color.white,
            radius=beam_radius,
            ballv=vec(cos(-angle), sin(-angle), 0),
            ballpos=_pos
        )
        self.beams = [
            [cylinder(pos=_pos, color=color.red,
                      radius=beam_radius, visible=False)],
            [cylinder(pos=_pos, color=color.orange,
                      radius=beam_radius, visible=False)],
            [cylinder(pos=_pos, color=color.yellow,
                      radius=beam_radius, visible=False)],
            [cylinder(pos=_pos, color=color.green,
                      radius=beam_radius, visible=False)],
            [cylinder(pos=_pos, color=color.blue,
                      radius=beam_radius, visible=False)],
            [cylinder(pos=_pos, color=color.purple,
                      radius=beam_radius, visible=False)]
        ]

    # does refract if there is one
    # param type = 'in' or 'out'
    def refract(self, droplet_pos, droplet_r):
        for i in range(6):
            if not self.in_lens[i] and self.reflected[i] == 0 and mag(droplet_pos - self.pos[i]) <= droplet_r:
                type = 'in'
                self.in_lens[i] = True
                self.log[i].append(self.pos[i])
                self.white.ballv = vec(0, 0, 0)
                self.white.axis = self.white.ballpos - self.white.pos
            elif self.in_lens[i] and self.reflected[i] >= 1 and mag(droplet_pos - self.pos[i]) >= droplet_r:
                type = 'out'
                self.in_lens[i] = False
                self.log[i].append(self.pos[i])
                self.beams[i].append(
                    cylinder(
                        pos=self.log[i][1],
                        color=self.beams[i][0].color,
                        radius=self.beams[i][0].radius,
                        axis=self.log[i][2] - self.log[i][1]
                    )
                )
                self.beams[i].append(
                    cylinder(
                        pos=self.log[i][2],
                        color=self.beams[i][0].color,
                        radius=self.beams[i][0].radius,
                        axis=self.pos[i] - self.log[i][2]
                    )
                )
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
            self.pos[i] += self.v[i] * 0.1
            print('refract!', i, self.pos[i])

    def reflect(self, droplet_pos, droplet_r):
        for i in range(6):
            if self.in_lens[i] and self.reflected[i] == 0 and mag(droplet_pos - self.pos[i]) >= 0.999 * droplet_r:
                self.reflected[i] += 1
                #  show the beam from refraction point to reflection point
                self.log[i].append(self.pos[i])
                self.beams[i][0].pos = self.log[i][0]
                self.beams[i][0].axis = self.log[i][1] - self.log[i][0]
                self.beams[i][0].visible = True

                normal_v = norm(droplet_pos - self.pos[i])
                angle_out = diff_angle(-self.v[i], normal_v)
                self.v[i] = rotate(normal_v, angle=angle_out,
                                   axis=cross(normal_v, self.v[i]))
                self.pos[i] += self.v[i] * 0.1
                print(f'reflect {i}')

    def update(self, droplet_pos, droplet_r):
        for i in range(6):
            self.refract(droplet_pos, droplet_r)
            self.reflect(droplet_pos, droplet_r)
            if len(self.beams[i]) >= 3:
                self.beams[i][2].axis = self.pos[i] - self.log[i][2]
        self.pos += self.v * self.dt
        self.white.ballpos += self.white.ballv * self.dt

    def run(self, droplet_pos, droplet_r):
        pos + t*v = sqrt(x**2 )


scene = canvas(background=vec(0.5, 0.5, 0.5), width=1200,
               height=600, center=vec(0, 0, 0))

# bg = box(pos=vec(0, 0, 0), size=vec(
# 20, 10, 0.0001), color=vec(0.2, 0.5, 0.5))
# droplet radius
r = 5
droplet = sphere(
    radius=r,
    pos=vec(0, 0, 0),
    color=vec(195/255, 253/255, 255/255),
    opacity=0.2
)
dropletCenter = sphere(radius=0.05, pos=droplet.pos, color=color.red)


def run(slider):
    angle = slider.value
    for position in range(3, 9):
        ray = Ray(rotate(vec(-8, position/2, 0), -angle), 0)
        done = False
        while not done:
            rate(10000)
            ray.update(droplet.pos, droplet.radius)

            for i in range(6):
                if mag(ray.pos[i]) >= 15:
                    print(i, ray.pos[i].y)
                    done = True
                    break


angle_slider = slider(vertical=True, max=pi/2, value=0,
                      bind=run, align='left', pos=scene.title_anchor)
