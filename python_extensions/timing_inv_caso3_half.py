
import numpy as np
from numpy.linalg import inv
from time import perf_counter
from numpy import geomspace
from scipy import linalg

def generar_matriz (N,dtype):
    L=np.zeros((N,N),dtype=dtype)
    np.fill_diagonal(L, dtype(2))
    b= -np.ones(N-1,dtype=dtype)
    np.fill_diagonal(L[1:], b)
    np.fill_diagonal(L[:,1:], b)
    return L


def memory_time_numpy (N,dtype): # numpy inverse
    L = generar_matriz(N, dtype)
    t1 = perf_counter()
    I = inv(L)
    t2 = perf_counter()
    malloc = L.nbytes + I.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)
    

def memory_time_scipy_f (N,dtype): #scipy inv overwrite_a=False
    L = generar_matriz(N, dtype)
    t1 = perf_counter()
    I = linalg.inv(L,overwrite_a=False)
    t2 = perf_counter()
    malloc = L.nbytes + I.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)
    

def memory_time_scipy_t (N,dtype): #scipy inv overwrite_a=True
    L = generar_matriz(N, dtype)
    t1 = perf_counter()
    I = linalg.inv(L,overwrite_a=True)
    t2 = perf_counter()
    malloc = L.nbytes + I.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)


output_file = open("output_file_timing_inv_caso3_half.txt","w")
output_file.write("Tiempo [segundos] Memoria [MB] Tamaño [N]\n") #header of the txt file

for corridas in range(1,10+1):
    output_file.write(f"Corrida {corridas}:\n")
    anterior = False
    for i in geomspace(1, 20_000,20):
        actual = int(i)
        if anterior == actual:
            pass
        else:
            dt, malloc = memory_time_scipy_t(int(i),np.half)
            print(f" N: {int(i)} ---> {dt:.6f} segundos  {malloc:.6f} MB")
            output_file.write(f"  {dt:.6f}         {malloc:.6f}         {int(i)} \n")
        anterior = actual
        


output_file.write("EOF\n")
output_file.close ()