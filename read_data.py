import sys
from numpy import genfromtxt


class read_data:
    # Class that reads the parameter file
    def read_file(self):
        """ Class that reads the parameter file
            - Reads the player names
            - Reads the parameters for each player
        """
        try:
            projectile_input = genfromtxt('projectile_input.csv', delimiter=',', skip_header=True)[:, 1:]
            names = genfromtxt('projectile_input.csv', delimiter=',', usecols=0, skip_header=True, dtype=str)

            return projectile_input, names
        except:
            print('File not available or format is not the expected')
            sys.exit(1)
