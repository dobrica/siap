import subprocess
import scipy
import numpy
import pandas
import itertools

print("\n")
print("Environment test: \n")
subprocess.call(['python', '--version'])
print("\n")
subprocess.call(['pip', '--version'])
print("\n")
print("Scipy version: " + scipy.version.version)
print("\n")
print("Numpy version: " + numpy.version.version)
print("\n")
print("Pandas version: " + pandas.__version__)
print("\n")
print("Installed" )
subprocess.call(['pip', 'list'])