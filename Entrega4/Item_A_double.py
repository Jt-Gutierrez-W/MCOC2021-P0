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

def caso_1 (N,dtype): 
    b=np.ones(N,dtype=dtype)
    A = generar_matriz(N, dtype)
    t1 = perf_counter()
    I = inv(A)
    x=I@b
    t2 = perf_counter()
    malloc = A.nbytes + I.nbytes + x.nbytes + b.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)

def caso_2 (N,dtype):
    b = np.ones(N,dtype=dtype)
    A = generar_matriz(N, dtype=dtype)
    t1 = perf_counter()
    x = linalg.solve(A,b)
    t2 = perf_counter()
    malloc = b.nbytes + A.nbytes + x.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)

def caso_3 (N,dtype):
    b = np.ones(N,dtype=dtype)
    A = generar_matriz(N, dtype=dtype)
    t1 = perf_counter()
    x = linalg.solve(A,b,assume_a='pos')
    t2 = perf_counter()
    malloc = b.nbytes + A.nbytes + x.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)
    
def caso_4 (N,dtype):
    b = np.ones(N,dtype=dtype)
    A = generar_matriz(N, dtype=dtype)
    t1 = perf_counter()
    x = linalg.solve(A,b,assume_a='sym')
    t2 = perf_counter()
    malloc = b.nbytes + A.nbytes + x.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)

def caso_5 (N,dtype):
    b = np.ones(N,dtype=dtype)
    A = generar_matriz(N, dtype=dtype)
    t1 = perf_counter()
    x = linalg.solve(A,b,overwrite_a=True)
    t2 = perf_counter()
    malloc = b.nbytes + A.nbytes + x.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)


def caso_6 (N,dtype):
    b = np.ones(N,dtype=dtype)
    A = generar_matriz(N, dtype=dtype)
    t1 = perf_counter()
    x = linalg.solve(A,b,overwrite_b=True)
    t2 = perf_counter()
    malloc = b.nbytes + A.nbytes + x.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)


def caso_7 (N,dtype):
    b = np.ones(N,dtype=dtype)
    A = generar_matriz(N, dtype=dtype)
    t1 = perf_counter()
    x = linalg.solve(A,b,overwrite_a=True,overwrite_b=True)
    t2 = perf_counter()
    malloc = b.nbytes + A.nbytes + x.nbytes
    dt = t2-t1
    return dt, malloc/(10**6)

def escribir_corrida (caso, file,dtype):
    time = [0]*20; mem = [0]*20; Ns= [0]*20; 
    for corridas in range(1,10+1):
        cont = 0
        anterior = False
        for i in geomspace(2, 5_000,20):
            actual = int(i)
            if anterior == actual:
                pass
            else:
                dt, malloc = caso(int(i),dtype)
                time[cont]+= dt; mem[cont]+= malloc; Ns[cont]+=int(i)
                cont+=1
                
                print(f" N: {int(i)} ---> {dt:.6f} segundos  {malloc:.6f} MB")
                
            anterior = actual
    output_file.write(f"Corrida A {caso.__name__} {dtype.__name__}:\n")   
    time = [tiempo/10 for tiempo in time]; mem = [memoria/10 for memoria in mem]; Ns = [size/10 for size in Ns]
    for i in range (len(time)):
        output_file.write(f"  {time[i]:.6f}         {mem[i]:.6f}         {int(Ns[i])} \n")
    return 
        
    
    
## MAIN ##
output_file = open("output_file_A_double.txt","w")
output_file.write("Tiempo [segundos] Memoria [MB] Tamaño [N]\n") #header of the txt file


cases = [caso_1,caso_2,caso_3,caso_4,caso_5,caso_6,caso_7]


for casos in cases:
    
    escribir_corrida(casos, output_file, np.double)
    
 

output_file.write("EOF\n")
output_file.close ()





    