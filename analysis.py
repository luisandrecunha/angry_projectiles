# calculate ball's projectile motion in both vacuum and with air resistance
#    returns time(T), x-position(X), and y-position(Y)
#
# methods
#   motion.velocity
#       calcuate object's speed, and velocity in both x-, y-direction
#
#   motion.accerleration
#       calcuate object's magnitude of acceleration, and acceleration in 
#       both x-, y-direction
#
#   motion.getMaxHeight
#       calcuate object's highest position
#
#   motion.NewtonMethod
#       Newton's method to find the root

from numpy import linspace
from numpy import average
from numpy import sqrt
from numpy import power as pow
from scipy.interpolate import interp1d
from statistics import median

class motion:
    def velocity(self, T, X, Y):
        # increase sample size of T (time) by twice
        Ti = linspace(T[0], T[-1], 2 * T.size - 1)
        dt = Ti[1] - Ti[0] # calculate delta time
        
        # calculate velocity in x-direction
        fX   = interp1d(T, X, kind='quadratic') # interplolate x-function
        Xi   = fX(Ti)
        dx   = Xi[1:Xi.size] - Xi[0:Xi.size-1]
        dxdt = dx / dt
        vx   = average(dxdt[1:-1].reshape([int((dxdt.size-2)/2), 2]), axis=1)
        
        # calculate velocity in y-direction
        fY   = interp1d(T, Y, kind='quadratic') # interplolate y-function
        Yi   = fY(Ti)
        dy   = Yi[1:Yi.size] - Yi[0:Yi.size-1]
        dydt = dy / dt
        vy   = average(dydt[1:-1].reshape([int((dydt.size-2)/2), 2]), axis=1)
        
        # get the magnitude
        t = T[1:T.size-1]
        v = sqrt(pow(vx, 2) + pow(vy, 2))
        
        return t, v, vx, vy
        
    def acceleration(self, T, X, Y):
        # calculate the velocity of the object
        Tv, V, Vx, Vy = self.velocity(self, T, X, Y)
        
        # increase sample size of T (time) by twice
        Tvi = linspace(Tv[0], Tv[-1], 2 * Tv.size - 1)
        dt  = Tvi[1] - Tvi[0] # calculate delta time
        
        # calculate accelration in x-direction
        fX    = interp1d(Tv, Vx, kind='quadratic') # interplolate x- velocity function
        Vxi   = fX(Tvi)
        dvx   = Vxi[1:Vxi.size] - Vxi[0:Vxi.size-1]
        dvxdt = dvx / dt
        ax    = average(dvxdt[1:-1].reshape([int((dvxdt.size-2)/2), 2]), axis=1)
        
        # calculate accelration in y-direction
        fY    = interp1d(Tv, Vy, kind='quadratic') # interplolate y-velocity function
        Vyi   = fY(Tvi)
        dvy   = Vyi[1:Vyi.size] - Vyi[0:Vyi.size-1]
        dvydt = dvy / dt
        ay    = average(dvydt[1:-1].reshape([int((dvydt.size-2)/2), 2]), axis=1)
        
        # get the magnitude
        t = Tv[1:Tv.size-1]
        a = sqrt(pow(ax, 2) + pow(ay, 2))
        
        return t, a, ax, ay

    def getMaxHeight(self, T, X, Y):
        # get velocity and accerlation
        Tv, V, Vx, Vy = self.velocity(self, T, X, Y)
        Ta, A, Ax, Ay = self.acceleration(self, T, X, Y)
        
        # interpolate the velocity and acceraltion function
        fvY  = interp1d(Tv, Vy, kind='quadratic')
        faY  = interp1d(Ta, Ay, kind='quadratic')
        tmax = self.NewtonMethod(self, fv=fvY, fa=faY, x0=median(Tv)) # newton's method
        
        return tmax
        
    def NewtonMethod(self, fv, fa, x0, tol=0.001):
        x1 = x0 - fv(x0) / fa(x0)
        x2 = x1 - fv(x1) / fa(x1)
        
        if abs(x1 - x2) > tol: # recursive function
            y = self.NewtonMethod(self, fv, fa, x0=x1)
        else:
            y = x0
            
        return y