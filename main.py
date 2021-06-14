from cylidericalRay import *


scene = canvas(
    background=vec(1, 1, 1),
    width=800,
    height=400,
    center=vec(0, 0, 0),
    range=10,
    userspin=False,
    userpan=False,
    userzoom=True,
    title='droplet',
    align='left'
)

y_to_amplitude = graph(
    align="right",
    xtitle="y/R",
    ytitle="relative amplitude of red and violet",
    background=vector(0.8, 0.8, 0.8)
)

y_to_angle = graph(
    align="right",
    xtitle="y/R",
    ytitle="angle (degree)",
    background=vector(0.8, 0.8, 0.8)
)

red_amp = gcurve(color=color.red, graph=y_to_amplitude)
vlt_amp = gcurve(color=color.purple, graph=y_to_amplitude)
red_ang = gcurve(color=color.red, graph=y_to_angle)
vlt_ang = gcurve(color=color.purple, graph=y_to_angle)

r = 5
droplet = sphere(
    radius=r,
    pos=vec(0, 0, 0),
    color=vec(195/255, 253/255, 255/255),
    opacity=0.1
)
dropletCenter = sphere(radius=0.05, pos=droplet.pos, color=color.red)

ray_arr = []

def run(slider):
    global red_amp, vlt_amp, red_ang, vlt_ang
    if len(ray_arr) != 0:
        while len(ray_arr) != 0:
            del ray_arr[0]
    if red_amp != None:
        red_amp.visible=False
        vlt_amp.visible=False
        red_ang.visible=False
        vlt_ang.visible=False
        del red_amp
        del vlt_amp
        del red_ang
        del vlt_ang
        red_amp = gcurve(color=color.red, graph=y_to_amplitude)
        vlt_amp = gcurve(color=color.purple, graph=y_to_amplitude)
        red_ang = gcurve(color=color.red, graph=y_to_angle)
        vlt_ang = gcurve(color=color.purple, graph=y_to_angle)
    for i in range(8):
        ray_arr.append(Ray(vec(-8, (i+2)/2, 0), slider.value))
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
                    y_dist = ray_arr[i].incidence_y/r
                    red_amp.plot(y_dist, ray_arr[i].beams[0][2].opacity)
                    vlt_amp.plot(y_dist, ray_arr[i].beams[5][2].opacity)
                    red_ang.plot(y_dist, ray_arr[i].exit_angles[0])
                    vlt_ang.plot(y_dist, ray_arr[i].exit_angles[1])
                    break
                # except Exception as e:
                #     pass


angle_slider = slider(vertical=True, max=pi/2, min=0,
                      bind=run, align='left', pos=scene.title_anchor)

run(angle_slider)
