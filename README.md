# Angry Projectiles

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


## Instructions to run:

1 - Before run the python code, you should define the parameters on projectile_input.csv file, as follows:
 - Your Name
 - Initial projectile speed
 - Initial projectile angle
 - If you use a customized object type (obj_type=0), then you need to define the following parameters:
 	- Drag coefficient
 	- Diameter
 	- Area
 	- Mass
 - Pick the object type that you want to use:
 	- 0 - Customized object type
 	- 1 - Sphere - Mass: 1kg; Area: 0.05m2; Drag Coefficient: 0.47
 	- 2 - Cube - Mass: 1kg; Area: 0.05m2; Drag Coefficient: 1.05
 	- 3 - Stream Lined Body - Mass: 0.04kg; Area: 0.04m2; Drag Coefficient: 0.04

2 - Run the python code:

	- Using terminal:
		1. python main.py
		2. python example.py

 	- Using an IDE:
		1. Edit "projectile_input.csv"
		2. Open "main.py" and run
		3. Open "example.py" and run

## More informations:

### Platform and Python Version:
PyCharm with Python 3.7.x

External packages used:
 - numpy v.1.15.4
 - scipy v.1.1.0
 - matplotlib v.3.0.2
 - statistics v.3.6

### Files:
main.py
	- import data and call functions from other files
	- defines a dictionary for possible objects to be used
	- plots a basket, which players will try to throw their object into
	- renders all projectile trajectories 
	- displays a dynamic process of projectile motions using animation
	- identifies the winner

	packages and methods used:
		1. Numpy
		2. matplotlib.pyplot
		3. FuncAnimation from matplotlib.animation

projectile_input.csv
	- text input file from user

example.py
	- demostrate an example of throwing a baseball with and without air resistance
	- calculate baseball's velocity and acceleration base on its motion trajectory
	- calculate baseball's highest (y-position)

	packages and methods used:
		1. constant pi (3.14) from SciPy
		2. interploation (interp1d) from SciPy
		3. plotting methods from matplotlib

read_data.py
	- reads projectile parameteres from csv file
	
	package and methods used:
		1. NumPy

objects.py
	- contains differernt shaped objects (sphere, cube, cone and etc) with its
		physical properties (initial x-, y-position, mass, drag coefficient, 
		and reference area)
	
projectile.py
	- calculate ball's projectile motion in both vacuum and with air resistance
	- returns time(T), x-position(X), and y-position(Y)
	- determines whether an object falls into the basket or not, and displays "Win" or "Fail"
	- stops the object if it hits the edge of the basket
	
	packages and methods used:
		1. math functions (sin, cos, deg2rad, sqrt, and exp) from NumPy
		2. array object from NumPy
		3. created a function where all possible situations are listed and dealt with
		4. used three flags to mark where to break the animation (to stop the object)
		
analysis.py
	- calculate object's velocity and acceleration by object's position in time
	- calculate object's highest position and time by using Newton's method
	
	packages and methods used:
		1. linear interploate (linspace) from NumPy
		2. math functions (average, sqrt, power, and median) from 
			NumPy and statistics package
		3. interploation (interp1d) from SciPy