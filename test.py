from vpython import *

scene = canvas(background=vec(0.5, 0.5, 0.5), width=1200,
               height=600, center=vec(0, 0, 0))
ball = sphere()
l = label(text='test', pos=vec(2,2,2))

if input() == 'd':
    ball.visible = False
    del ball