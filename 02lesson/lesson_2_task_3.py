import math

def square(side):
    return math.ceil(side*side)


side = float (input("сторона квадрата:"))
print (f"площадь квадрата:{(square(side))}")