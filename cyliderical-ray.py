from vpython import *
import numpy as np

nair = 1.0
nwater = [1.3320, 1.3325, 1.3331, 1.3349, 1.3390, 1.3435]


class Ray:
    def __init__(self, _pos=vec(0, 0, 0), angle=0):
        _pos = rotate(_pos, -angle)
        self.pos = np.array([], dtype=vec)
        self.v = np.array([], dtype=vec)
        self.axis = []
        self.log = [[], [], [], [], [], []]
        self.opacity = [[], [], [], [], [], []]
        self.dt = 0.001

        self.in_lens = [False, False, False, False, False, False]
        self.reflected = [0, 0, 0, 0, 0, 0]

        self.angle_labels = []
        self.amplitude_labels = []

        for i in range(6):
            self.v = np.append(self.v, vec(cos(-angle), sin(-angle), 0))
            self.pos = np.append(self.pos, _pos)

        beam_radius = 0.05
        self.white = cylinder(
            pos=_pos,
            color=color.white,
            radius=beam_radius,
            axis=vec(0, 0, 0),
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
        def Rs(i, t): return (sin(t-i)/sin(t+i))**2
        def Rp(i, t): return (tan(t-i)/tan(t+i))**2
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
                        axis=self.log[i][2] - self.log[i][1],
                        opacity=self.opacity[i][1] * self.opacity[i][0]
                    )
                )
                print(
                    f'self.opacity[{i}][1] = {self.opacity[i][1] * self.opacity[i][0]}')
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
            angle_in = diff_angle(self.v[i], normal_v)
            angle_out = asin(n1 / n2 * sin(angle_in))
            self.opacity[i].append(
                1 - (Rs(angle_in, angle_out) + Rp(angle_in, angle_out)) / 2)
            self.v[i] = rotate(
                normal_v,
                angle=angle_out,
                axis=cross(normal_v, self.v[i])
            )
            if type == 'out' and (i == 0 or i == 5) and len(self.beams[i]) == 3:
                self.angle_labels.append(label(
                    pos=self.beams[i][2].pos + self.beams[i][2].axis / 2,
                    text="{0:4.2f}deg".format(diff_angle(
                        self.v[i], -self.white.axis) * 180/pi),
                    xoffset=20 if i == 0 else -20,
                    yoffset=-5 if i == 0 else 5
                ))
            self.pos[i] += self.v[i] * 0.1

    def reflect(self, droplet_pos, droplet_r):
        def Rs(i, t): return (sin(t-i)/sin(t+i))**2
        def Rp(i, t): return (tan(t-i)/tan(t+i))**2
        for i in range(6):
            if self.in_lens[i] and self.reflected[i] == 0 and mag(droplet_pos - self.pos[i]) >= 0.999 * droplet_r:
                self.reflected[i] += 1
                #  show the beam from refraction point to reflection point
                self.log[i].append(self.pos[i])
                self.beams[i][0].pos = self.log[i][0]
                self.beams[i][0].axis = self.log[i][1] - self.log[i][0]
                self.beams[i][0].opacity = self.opacity[i][0]
                print(f'self.opacity[{i}][0] = {self.opacity[i][0]}')
                self.beams[i][0].visible = True

                normal_v = norm(droplet_pos - self.pos[i])
                angle_in = diff_angle(-self.v[i], normal_v)
                angle_out = asin(nwater[i] / nair * sin(angle_in))
                self.opacity[i].append(
                    (Rs(angle_in, angle_out) + Rp(angle_in, angle_out)) / 2)

                angle_ref = diff_angle(-self.v[i], normal_v)
                self.v[i] = rotate(normal_v, angle=angle_ref,
                                   axis=cross(normal_v, self.v[i]))
                self.pos[i] += self.v[i] * 0.1
                # print(f'reflect {i}')

    def update(self, droplet_pos, droplet_r):
        for i in range(6):
            self.refract(droplet_pos, droplet_r)
            self.reflect(droplet_pos, droplet_r)
            if len(self.beams[i]) >= 3:
                self.beams[i][2].axis = self.pos[i] - self.log[i][2]
            if len(self.angle_labels) >= 1:
                self.angle_labels[0].pos = self.beams[0][2].pos + \
                    self.beams[0][2].axis / 2
            if len(self.angle_labels) >= 2:
                if self.beams[i][2].opacity == 1:
                    self.beams[i][2].opacity = self.opacity[i][0] * \
                        self.opacity[i][1] * self.opacity[i][2]
                    print(f'self.opacity[{i}][2] = {self.opacity[i][0] * self.opacity[i][1] * self.opacity[i][2]}')
                self.angle_labels[1].pos = self.beams[5][2].pos + \
                    self.beams[5][2].axis / 2
        self.pos += self.v * self.dt
        self.white.ballpos += self.white.ballv * self.dt

    def __del__(self):
        self.white.visible = False
        del self.white
        while len(self.angle_labels) != 0:
            self.angle_labels[0].visible = False
            del self.angle_labels[0]
        for i in range(6):
            while len(self.beams[i]) != 0:
                self.beams[i][0].visible = False
                del self.beams[i][0]


scene = canvas(
    background=vec(1, 1, 1),
    width=1200,
    height=600,
    center=vec(0, 0, 0),
    range=10,
    userspin=False,
    userpan=False,
    userzoom=True,
    title='droplet',
    align='left'
)

r = 5
droplet = sphere(
    radius=r,
    pos=vec(0, 0, 0),
    color=vec(195/255, 253/255, 255/255),
    opacity=0.1
)
dropletCenter = sphere(radius=0.05, pos=droplet.pos, color=color.red)

ray_arr = []

def run2(slider):
    if len(ray_arr) != 0:
        while len(ray_arr) != 0:
            del ray_arr[0]
    for i in range(7):
        ray_arr.append(Ray(vec(-8, (i+2.5)/2, 0), slider.value))
        done = False
        while not done:
            rate(10000)
            # try:
            ray_arr[i].update(droplet.pos, droplet.radius)
            # except Exception as e:
            #     pass
            for j in range(6):
                # try:
                if mag(ray_arr[i].pos[j]) >= 15:
                    done = True
                    break
                # except Exception as e:
                #     pass


angle_slider = slider(vertical=True, max=pi/2, min=0,
                      bind=run2, align='left', pos=scene.title_anchor)

slider.value = 0
