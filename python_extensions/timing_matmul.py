from numpy.random import rand
from time import perf_counter
from numpy import geomspace

output_file = open("output_file_timing_matmul.txt","w")
output_file.write("Tiempo [segundos] Memoria [MB] Tamaño [N]\n") #header of the txt file

def malloc_time (N): #this function returns the time and memory allocation of the mat multiplication.
    A = rand(N,N)
    B = rand(N,N)
    
    t1 = perf_counter()
    C = A@B
    t2 = perf_counter()
    malloc = A.nbytes + B.nbytes + C.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)
 


for corridas in range (1,10+1):
    output_file.write(f"Corrida {corridas}:\n")
    anterior = False
    for i in geomspace(1, 20_000,30):
        actual = int(i)
        if anterior == actual:
            pass
        else:
            dt, malloc = malloc_time(int(i))
            print(f" N: {int(i)} ---> {dt:.6f} segundos  {malloc:.6f} MB")
            output_file.write(f"  {dt:.6f}         {malloc:.6f}         {int(i)} \n")
        anterior = actual
    
output_file.write("EOF\n")
output_file.close ()



