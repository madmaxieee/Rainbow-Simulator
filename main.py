from cylidericalRay import *

y_to_amplitude = graph(xtitle="y/R",
                       ytitle="relative amplitude of red and violet",
                       background=vector(0.8, 0.8, 0.8))

y_to_angle = graph(xtitle="y/R",
                   ytitle="angle (degree)",
                   background=vector(0.8, 0.8, 0.8))

red_amp = gcurve(color=color.red, graph=y_to_amplitude)
red_amp_dot = gdots(color=color.red, graph=y_to_amplitude)
vlt_amp = gcurve(color=color.purple, graph=y_to_amplitude)
vlt_amp_dot = gdots(color=color.purple, graph=y_to_amplitude)
red_ang = gcurve(color=color.red, graph=y_to_angle)
red_ang_dot = gdots(color=color.red, graph=y_to_angle)
vlt_ang = gcurve(color=color.purple, graph=y_to_angle)
vlt_ang_dot = gdots(color=color.purple, graph=y_to_angle)


def run_droplet(slider):
    global red_amp, vlt_amp, red_ang, vlt_ang, red_amp_dot, vlt_amp_dot, red_ang_dot, vlt_ang_dot
    if len(ray_arr) != 0:
        while len(ray_arr) != 0:
            del ray_arr[0]
    if red_amp != None:
        red_amp.visible = False
        vlt_amp.visible = False
        red_ang.visible = False
        vlt_ang.visible = False
        del red_amp
        del vlt_amp
        del red_ang
        del vlt_ang
        del red_amp_dot
        del vlt_amp_dot
        del red_ang_dot
        del vlt_ang_dot
        red_amp = gcurve(color=color.red, graph=y_to_amplitude)
        red_amp_dot = gdots(color=color.red, graph=y_to_amplitude)
        vlt_amp = gcurve(color=color.purple, graph=y_to_amplitude)
        vlt_amp_dot = gdots(color=color.purple, graph=y_to_amplitude)
        red_ang = gcurve(color=color.red, graph=y_to_angle)
        red_ang_dot = gdots(color=color.red, graph=y_to_angle)
        vlt_ang = gcurve(color=color.purple, graph=y_to_angle)
        vlt_ang_dot = gdots(color=color.purple, graph=y_to_angle)
    for i in range(16):
        ray_arr.append(Ray(vec(-8, (i + 4) / 4, 0), slider.value))
        done = False
        while not done:
            rate(10000)
            try:
                ray_arr[i].update(droplet.pos, droplet.radius)
                for j in range(6):
                    if mag(ray_arr[i].pos[j]) >= 15:
                        done = True
                        y_dist = ray_arr[i].incidence_y / r
                        red_amp.plot(y_dist, ray_arr[i].beams[0][2].opacity)
                        red_amp_dot.plot(y_dist, ray_arr[i].beams[0][2].opacity)
                        vlt_amp.plot(y_dist, ray_arr[i].beams[5][2].opacity)
                        vlt_amp_dot.plot(y_dist, ray_arr[i].beams[5][2].opacity)
                        red_ang.plot(y_dist, ray_arr[i].exit_angles[0])
                        red_ang_dot.plot(y_dist, ray_arr[i].exit_angles[0])
                        vlt_ang.plot(y_dist, ray_arr[i].exit_angles[1])
                        vlt_ang_dot.plot(y_dist, ray_arr[i].exit_angles[1])
                        break
            except IndexError:
                pass
            except ValueError:
                pass


slider_label = wtext(
    text='',
    pos=scene.title_anchor,
)


def run(slider):
    slider_label.text = '{0:3.1f}'.format(slider.value * 180 / pi) + 'deg'
    rotate_rainbow(slider)
    run_droplet(slider)


angle_slider = slider(vertical=True,
                      max=pi / 2,
                      min=0,
                      bind=run,
                      align='left',
                      pos=scene.title_anchor)

from rainbow import *

run(angle_slider)
