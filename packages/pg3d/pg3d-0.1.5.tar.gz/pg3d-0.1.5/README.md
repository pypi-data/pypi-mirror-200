# PG3D

PG3D is a simple 3D graphics library written using Pygame.


## Installation
---
1) Install Python 3.7 or newer. https://www.python.org/downloads/
2) Open cmd/terminal and type:
```
pip install pg3d
```

## Dependencies
---
* python 3.7+
* pygame

## Usage
---
1) Import the library
```py
from pg3d import *
```
2) Create an App instance and call the run function
```py
app = App()

#---Code goes here---#

#--------------------#

app.run()
```

## API Reference
---
```py
App(kwargs):


kwargs:
    dimensions=(1000, 700)
    cam_pos=[0, 0, 0]
    BG_COLOR=(0, 0, 0)
    LINE_COLOR=(255, 255, 255) 
    VERTEX_SIZE=2              
    stats=False                # Show stats on screen
    fullscreen=False           
    mouse_look=False           # Use mouse for camera orientation


functions:
    run()  # Draws all vertices and checks for movement
```
---
```py
Model(args)


args:
    app   # Specify the App() object
    path  # Specify path of .obj file
```
---
```py
Shape(args, kwargs)


args:
    app    # Specify the App() object
    shape  # "cube" | "pyramid" | "tetrahedron"


kwargs:
    size=1
    center=[0, 0, 0]
    width=1
```
---
```py
Triangle(args)


args:
    app       # Specify the App() object
    vertices  # List or tuple with 3 cartesian coordinates


functions:
    __getitem__(index)  # Returnes indext point of Triangle object
```
---
```py
Point(args, kwargs)


args:
    app         # Specify the App() object
    coordinate  # A list with a single cartesian coordinate


kwargs:
    vertex=True  # If true the point is drawn and vice versa


functions:
    __repr__()                 # Prints Point object
    __setitem__(index, value)  # Sets indexed coordinate of Point object to value
    __getitem__(index)         # Returns indexed coordinate of Point object
```
---
```py
Matrix(args)


args:
    matrix  # A 2D array


functions:
    __repr__()                 # Prints a Matrix object
    __setitem__(index, value)  # Sets indexed value of Matrix object to value
    __getitem__(index)         # Returns value of indexed Matrix object
    __rmul__(value)            # Returns product of Matrix object and number
    __mul__(other)             # Multiplies 2 matrices together
    __add__(other)             # Adds 2 matrices together
    __sub__(other)             # Subtracts 2 matrices together
    transpose()                # Transposes Matrix object
    determinant()              # Finds determinant of Matrix object
    inverse()                  # Finds inverse of Matrix object
    is_square()                # Checks whether matrix is square or not

```