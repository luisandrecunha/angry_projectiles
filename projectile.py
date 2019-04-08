from numpy import cos as cos
from numpy import sin as sin
from numpy import deg2rad as deg2rad
from numpy import sqrt as sqrt
from numpy import exp as exp
from numpy import array as array

g = -9.81 # gravitational acceleration, m/s^2
p = 1.225 # density of the air, kg/m^3
basket_height = 50
basket_bottom = 0
left_bar = 400
right_bar = 500

class motion:
    """ Class that calculates and returns the trajectory of the object based on:
        - Object type (mass, area)
        - Initial speed and angle
        - Drag or Vacuum
    """
    def Vacuum(self, obj, v0=100, deg=45, dt=0.1):
        # Returns the trajectory on the vacuum
        theta = deg2rad(deg)
        vx = v0 * cos(theta) # velocity in x-direction
        vy = v0 * sin(theta) # velocity in y-direction

        t = 0.0
        x = obj.x0
        y = obj.y0

        T = [t]
        X = [x]
        Y = [y]

        while t==0.0 or y>0.0:
            t  += dt
            x  += vx * dt
            vy += g * dt
            y  += vy * dt
            T.append(t)
            X.append(x)
            Y.append(y)

        T = array(T)
        X = array(X)
        Y = array(Y)

        return T, X, Y

    def Drag(self, obj, v0=100, deg=45, dt=0.1, person='Undefined'):
        # Returns the trajectory when there is air resistance
        theta = deg2rad(deg)

        m  = obj.m
        Cd = obj.Cd
        A  = obj.A
        vt = sqrt((2 * m * abs(g)) / (p * A * Cd))

        t  = 0.0
        x0 = obj.x0
        y0 = obj.y0
        y  = y0

        T = [t]
        X = [x0]
        Y = [y0]

        passed_left = False  # two flags, for last time point, not the current one
        passed_right = False
        flag = False # indicate whether the object should stop moving
        result = ''

        while t==0.0 or y>0.0:
            t += dt
            x  = x0 + ((v0 * vt) / abs(g)) * cos(theta) * (1 - exp(g * t/vt))
            y  = y0 + (vt / abs(g)) * (v0 * sin(theta) + vt) * (1 - exp(g * t/vt)) - vt * t

            x, y, passed_left, passed_right, flag, result = self.failure(x, y, X, Y, passed_left, passed_right, flag, person)

            T.append(t)
            X.append(x)
            Y.append(y)
            if flag:
                break

        T = array(T)
        X = array(X)
        Y = array(Y)

        return T, X, Y, result

    def failure(self, x, y, X, Y, passed_left, passed_right, flag, person):
        # Function that tests each trajectory to check if reached the target, only works for Drag conditions
        result = ''
        if y <= basket_bottom and x > 0 and y - Y[-1] < 0:
            if passed_left and not passed_right:
                print("%s - Success" %person)
                result = 'Win'
            else:
                print("%s - Failure" %person)
                result = 'Fail'
        else:
            # x happens to be at exactly 400
            if x == left_bar:
                if y <= basket_height:
                    print("%s - Failure" %person)
                    flag = True
                    result = 'Fail'
                else:
                    passed_left = True
                    result = 'Fail'
            # more common case since Xs are discrete points
            elif x > left_bar and not passed_left:
                y_at_400 = (y - Y[-1]) / (x - X[-1]) * (left_bar - X[-1]) + Y[-1]
                if y_at_400 <= basket_height:
                    print("%s - Failure" %person)
                    x = left_bar
                    y = y_at_400
                    flag = True
                    result = 'Fail'
                else:
                    passed_left = True
                    result = 'Fail'
            # x happens to be at exactly 600
            elif x == right_bar:
                if y < basket_height:
                    print("%s - Success" %person)
                    result = 'Win'
                    flag = True
            # more common case
            elif x > right_bar and not passed_right:
                y_at_600 = (y - Y[-1]) / (x - X[-1]) * (right_bar - X[-1]) + Y[-1]
                if y_at_600 > basket_height:
                    passed_right = True
                    result = 'Fail'
                else:
                    print("%s - Success" %person)
                    x = right_bar
                    y = y_at_600
                    flag = True
                    result = 'Win'
        return x, y, passed_left, passed_right, flag, result
