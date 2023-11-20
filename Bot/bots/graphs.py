__author__ = 'Ryan'
import matplotlib.pyplot as plt
import numpy as np

# usage: takes in an array of data
# output: saves the histogram to the file
def histogram(dataArray, path: str):
    plt.hist(dataArray)
    plt.savefig(path)

# usage: takes in an equation (a lambda function, i made functions to create these) and the x range (use range(a, b))
# output: saves the plot to the png file
def plotter(equation, x_range, path: str):
    x = np.array(x_range)  
    y = equation(x)  
    plt.plot(x, y)  
    plt.savefig(path)  

def equationMakerAB(a, b):
    return lambda x: a*x + b

def equationMakerABC(a, b, c):
    return lambda x: (a*x)**2 + b*x + c

def equationMakerABCD(a, b, c, d):
    return lambda x: (a*x)**3 + (b*x)**2 + c*x + d

def equationMakerABCDE(a, b, c, d, e):
    return lambda x: (e*x)**4 + (d*x)**3 + (c*x)**2 + b*x + a

def main():
    # random_data = np.random.normal(170, 10, 250)
    # random_data = [1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,5]
    # histogram(random_data)
    equation = equationMakerABC(3, 2, 7)
    plotter(equation, range(-10, 11))

# main()