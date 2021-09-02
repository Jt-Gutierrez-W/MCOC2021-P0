
from time import perf_counter
from numpy import geomspace
import numpy as np
from scipy.sparse import diags
from scipy.linalg import solve
from scipy.sparse.linalg import spsolve

def generar_matriz_llena (N,dtype): #matriz llena estilo numpy clasico
    t1 = perf_counter()  
    L=np.zeros((N,N),dtype=dtype)
    np.fill_diagonal(L, dtype(2))
    np.fill_diagonal(L[1:], -np.ones(N-1,dtype=dtype))
    np.fill_diagonal(L[:,1:], -np.ones(N-1,dtype=dtype))
    t2 = perf_counter()
    dt = t2-t1
    return L, dt

def generar_matriz_sparse(N,dtype): 
    t1 = perf_counter()
    L = diags([-1, 2, -1], [-1, 0, 1], shape=(N, N),format="csr")
    t2 = perf_counter()
    dt = t2-t1
    return L, dt    
    
def solve_time_llena (N,dtype):
    b = np.ones(N,dtype=dtype)
    A,dt_E = generar_matriz_llena(N, dtype=dtype)
    t1 = perf_counter()
    solve(A,b)
    t2 = perf_counter()
    dt_S = t2-t1
    return dt_E, dt_S
 
def solve_time_sparse (N,dtype):
    b = np.ones(N,dtype=dtype)
    A,dt_E = generar_matriz_sparse(N, dtype=dtype)
    t1 = perf_counter()
    spsolve(A,b)
    t2 = perf_counter()
    dt_S = t2-t1
    return dt_E, dt_S


output_file = open("output_file_timing_solve_sparse.txt","w")
output_file.write("Tiempo E [segundos] Tiempo M [segundos] Tamaño [N]\n") #header of the txt file

for corridas in range (1,10+1):
    output_file.write(f"Corrida {corridas}:\n")
    anterior = False
    for i in geomspace(1, 20_000,25):
        actual = int(i)
        if anterior == actual:
            pass
        else:
            dt_G,dt_M = solve_time_sparse(int(i),np.double)
            print(f" N: {int(i)} ---> Ensamblaje {dt_G:.6f} segundos  Multiplicacion {dt_M:.6f} segundos")
            output_file.write(f"  {dt_G:.6f}         {dt_M:.6f}         {int(i)} \n")
        anterior = actual
    
output_file.write("EOF\n")
output_file.close ()

