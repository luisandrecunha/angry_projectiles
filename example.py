# demostrate an example of throwing a baseball with and without air resistance
# calculate baseball's velocity and acceleration base on its motion trajectory
# calculate baseball's highest (y-position)

import objects as obj
import projectile as proj
from analysis import motion as motionAnalysis
from scipy import pi as pi
from scipy.interpolate import interp1d
import pylab as plb

objmtn = proj.motion()

# example from http://dynref.engr.illinois.edu/afp.html
initial_speed = 30.0 # 30 m/s
initial_angle = 45.0 # 45 degree
drag_coefficient = 0.5
diameter = 0.075 # 7.5 cm
ref_area = (pi / 4) * diameter * diameter
mass = 0.145 # 145 g

baskball = obj.Custom(Cd=drag_coefficient, A=ref_area, mass=mass)
t1, x1, y1 = objmtn.Vacuum(baskball, v0=initial_speed, deg=initial_angle)
tv1, v1, vx1, vy1 = motionAnalysis.velocity(motionAnalysis, T=t1, X=x1, Y=y1)
ta1, a1, ax1, ay1 = motionAnalysis.acceleration(motionAnalysis, T=t1, X=x1, Y=y1)
t1max = motionAnalysis.getMaxHeight(motionAnalysis, T=t1, X=x1, Y=y1)

t2, x2, y2, dummy = objmtn.Drag(baskball, v0=initial_speed, deg=initial_angle, dt=0.1, person='Undefined')
tv2, v2, vx2, vy2 = motionAnalysis.velocity(motionAnalysis, T=t2, X=x2, Y=y2)
ta2, a2, ax2, ay2 = motionAnalysis.acceleration(motionAnalysis, T=t2, X=x2, Y=y2)
t2max = motionAnalysis.getMaxHeight(motionAnalysis, T=t2, X=x2, Y=y2)

fx = interp1d(t2, x2, kind='quadratic')
fy = interp1d(t2, y2, kind='quadratic')

# figure 1: position
plb.figure(figsize=(6 * 3.13, 4 * 3.13))
plb.plot(x2, y2, label='baseball', linestyle=':', marker='o')
plb.plot(fx(t2max), fy(t2max), label='highest point', linestyle='', marker='o', markersize=18)
plb.plot(x1, y1, label='baseball in vaccum', linestyle=':')
plb.annotate(r'$t_{ymax}=1.654s$',
             xy=[fx(t2max), fy(t2max)], xycoords='data', textcoords='offset points',
             xytext=(-25, 75), fontsize=20, color='black',
             arrowprops=dict(arrowstyle="-|>", color='black',
                             connectionstyle="arc3,rad=0.65"))
plb.xlim([0, 100])
plb.ylim([0, 30])
plb.grid(True)
plb.title('Projectiles of a baseball', fontsize=24)
plb.xlabel('horizontal x-position (m)', fontsize=18)
plb.ylabel('vertical y-position (m)', fontsize=18)
plb.legend(fontsize=18)

# figure 2: velocity
plb.figure(figsize=(6 * 3.13, 4 * 3.13))
plb.subplot(3, 1, 1)
plb.plot(tv2, v2, label='speed', linestyle=':', marker='s')
plb.grid(True)
plb.title('Speed of a baseball', fontsize=24)
plb.xlabel('time (s)', fontsize=18)
plb.ylabel('speed (m/s)', fontsize=10)
plb.legend(fontsize=18)

plb.subplot(3, 1, 2)
plb.plot(tv2, vx2, label='velocity x-direction', linestyle=':', marker='s')
plb.grid(True)
#plb.title('Velocity of a baseball in x-direction', fontsize=24)
plb.xlabel('time (s)', fontsize=18)
plb.ylabel('speed (m/s)', fontsize=10)
plb.legend(fontsize=18)

plb.subplot(3, 1, 3)
plb.plot(tv2, vy2, label='velocity y-direction', linestyle=':', marker='s')
plb.grid(True)
#plb.title('Velocity of a baseball in y-direction', fontsize=24)
plb.xlabel('time (s)', fontsize=18)
plb.ylabel('speed (m/s)', fontsize=10)
plb.legend(fontsize=18)

# figure 3: acceleration
plb.figure(figsize=(6 * 3.13, 4 * 3.13))
plb.subplot(3, 1, 1)
plb.plot(ta2, a2, label='acceleration', linestyle=':', marker='s')
plb.grid(True)
plb.title('Acceleration of a baseball', fontsize=24)
plb.xlabel('time (s)', fontsize=18)
plb.ylabel('accleration (m/s^2)', fontsize=10)
plb.legend(fontsize=18)

plb.subplot(3, 1, 2)
plb.plot(ta2, ax2, label='acceleration x-direction', linestyle=':', marker='s')
plb.grid(True)
#plb.title('Acceleration of a baseball in x-direction', fontsize=24)
plb.xlabel('time (s)', fontsize=18)
plb.ylabel('accleration (m/s^2)', fontsize=10)
plb.legend(fontsize=18)

plb.subplot(3, 1, 3)
plb.plot(ta2, ay2, label='acceleration y-direction', linestyle=':', marker='s')
plb.grid(True)
#plb.title('Acceleration of a baseball in y-direction', fontsize=24)
plb.xlabel('time (s)', fontsize=18)
plb.ylabel('accleration (m/s^2)', fontsize=10)
plb.legend(fontsize=18)
plb.show(block=True)