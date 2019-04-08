#!/usr/bin/env python

"""Project - Angry Projectiles -
    Simulate the launch and study the motion of a projectile, given some parameters like:
    - Object type
    - Mass
    - Area
    - Diameter
    - Initial speed
    - Initial Angle

    Project executed by:
    - Andy Tsai
    - Hongling Lei
    - Luis Cunha

"""

import objects as obj
import projectile as proj
from projectile import basket_height, left_bar, right_bar, basket_bottom
from read_data import read_data

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Defining dictionary for possible objects to be used.
name_dict = {
    0: "Custom Object",  # Defined in the input file
    1: "Sphere",  # Mass: 1kg         Area: 0.05m2    Drag Coefficient: 0.47
    2: "Cube",  # Mass: 1kg         Area: 0.05m2    Drag Coefficient: 1.05
    3: "StreamlinedBody",  # Mass: 0.04kg      Area: 0.04m2    Drag Coefficient: 0.04
}

func_dict = {
    0: obj.Custom,
    1: obj.Sphere,
    2: obj.Cube,
    3: obj.StreamlinedBody
}


class Renderer:
    """ Class responsible to render all projectiles trajectory
        - Read the parameters from file
        - For each ser of parameters, it gets the trajectory
        - Plot each trajectory in a chart with labels
        - Identifies the winner
    """

    def __init__(self):
        # Initialize all variables
        self.vacuum_simulation = False  # Vacuum simulation false for better game experience
        self.graph = None
        self.line_num = 1
        self.label_array = list([])
        self.x_array = []
        self.y_array = []
        self.x_max = 0
        self.y_max = 0
        self.mtn = proj.motion()
        self.reader = read_data()
        self.left_boundary = left_bar
        self.right_boundary = right_bar

    def get_x_y(self, arr, arr1):
        """ Get all values need to plot:
            - x_array: contain an array with all x values
            - y_array: contain an array with all y values
            - x_max: max value of x_array, to define plot's x axis limit
            - y_max: max value of x_array, to define plot's y axis limit
            - label_array: Labels for each array, to use in plot legend
        """
        for row in arr:
            # Set projectile parameters from input array, per row
            person_name = arr1[self.line_num - 1]
            initial_speed = row[0]
            initial_angle = row[1]
            drag_coefficient = row[2]
            diameter = row[3]
            ref_area = row[4] * diameter * diameter
            mass = row[5]
            objType = row[6]
            result = ''

            # Based on object type, it calls the customized or preset object
            if objType >= len(func_dict):
                raise Exception('Object type given is invalid')
            elif objType == 0:
                selected = func_dict[objType](Cd=drag_coefficient, A=ref_area, mass=mass)
            else:
                selected = func_dict[objType]()

            # Based on parameters and object, it calculates its trajectory
            # Get trajectory and set labels only for Drag trajectory:
            t1, x1, y1, result = self.mtn.Drag(selected, v0=initial_speed, deg=initial_angle, person=person_name)
            x2, y2 = np.array([0., 0.]), np.array([0., 0.])



            # If Vacuum simulation is true, then gets Vacuum trajectory and sets label:
            if self.vacuum_simulation == True:
                t2, x2, y2 = self.mtn.Vacuum(selected, v0=initial_speed, deg=initial_angle)

                self.label_array.append([str(person_name) + ' using a ' + name_dict[objType] + ' Speed: '
                                         + str(initial_speed) + ' Angle: ' + str(initial_angle) + ' Drag ' + str(result)])
                self.label_array.append([str(person_name) + ' using a ' + name_dict[objType] +
                                         ' Speed: ' + str(initial_speed) + ' Angle: ' + str(initial_angle) + ' Vacuum',
                                         ''])
            else:
                # Append labels to the array, to be plotted in the chart
                self.label_array.append([str(person_name) + ' using a ' + name_dict[objType] + ' Speed: '
                                         + str(initial_speed) + ' Angle: ' + str(initial_angle) + ' Drag ' + str(result)])
                self.label_array.append([''])

            # Append Vacuum and Drag trajectory values to final arrays
            self.x_array = np.append(self.x_array, np.array([x1, x2], dtype=object))
            self.y_array = np.append(self.y_array, np.array([y1, y2], dtype=object))

            # Defines chart boundaries based on max values
            # Set the axis X max value by getting the max value of x1 or x2
            if max(x1) > max(x2) and max(x1) > self.x_max:
                self.x_max = max(x1)
            elif max(x2) > max(x1) and max(x2) > self.x_max:
                self.x_max = max(x2)
            # Set the axis Y max value by  getting the max value of y1 or y2
            if max(y1) > max(y2) and max(y1) > self.y_max:
                self.y_max = max(y1)
            elif max(y2) > max(y1) and max(y2) > self.y_max:
                self.y_max = max(y2)

            # iterate the line_num
            self.line_num += 1

        # Return all need values to plot
        return self.label_array, self.x_array, self.y_array, self.x_max, self.y_max

    def init(self):
        """Initialize each plot line for chart
        """
        for line in self.graph:
            line.set_data([], [])
        return self.graph

    def animate(self, i):
        """Function to plot all projectile paths
        """
        item = 0

        # For each item in x_array (y_array could also be used)
        while item < len(self.x_array):
            # Add to the each graph the data to plot x and y points
            self.graph[item].set_data(self.x_array[item][:i], self.y_array[item][:i])
            # Add legend for each plot line
            self.graph[item].set_label('%s ' % self.label_array[item][0])

            # Iterator value depends on vacuum simulation flag
            if self.vacuum_simulation == True:
                item += 1
            else:
                item += 2

        # Plots the basket
        self.graph[item].set_data([left_bar, left_bar], [basket_bottom, basket_height])
        self.graph[item].set_color("black")
        self.graph[item + 1].set_data([left_bar, right_bar], [basket_bottom, basket_bottom])
        self.graph[item + 1].set_color("black")
        self.graph[item + 2].set_data([right_bar, right_bar], [basket_bottom, basket_height])
        self.graph[item + 2].set_color("black")

        # Set legend position
        legend = plt.legend(loc='upper left')
        return self.graph + [legend]

    def plot(self):
        """ Function that:
            - Gets the names and parameters from the file
            - Gets the trajectory of each projectile
            - Draw the trajectory with animation in a chart
        """
        # Read parameters from csv
        param_input, names = self.reader.read_file()

        # Get all data that will be used as parameters to create plot
        label_array, x_array, y_array, x_max, y_max = self.get_x_y(param_input, names)
        # Transform the labels list in an array
        label_array = np.asarray(label_array)

        # Plot definition
        fig = plt.figure(figsize=(6 * 3.13, 4 * 3.13))
        # Define different axes with limits defined by x_max and y_max
        ax = plt.axes(xlim=(0, x_max + 100), ylim=(0, y_max + 100))
        # Define plot line type
        self.graph = ax.plot(*([[], []] * (len(x_array) + 3)), marker=",")

        # Call animation function that will plot projectile lines in the chart
        # If blit = True, it produces a weird black horizontal and vertical banner
        ani = FuncAnimation(fig, self.animate, init_func=self.init, frames=1000, interval=1, blit=False, repeat=False)

        # Add title, axis labels and grid
        plt.grid(False)
        plt.title('Angry Projectiles')
        plt.ylabel('vertical position y / m')
        plt.xlabel('horizontal position x / m')

        plt.show()


renderer = Renderer()
renderer.plot()
