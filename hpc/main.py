import os

# loop to compute forever
while True:
    os.system("mpiexec -n 5 python .\compute.py")
