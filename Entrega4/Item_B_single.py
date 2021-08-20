import numpy as np
from scipy.linalg import eigh
from time import perf_counter
from numpy import geomspace


def generar_matriz (N,dtype):
    L=np.zeros((N,N),dtype=dtype)
    np.fill_diagonal(L, dtype(2))
    b= -np.ones(N-1,dtype=dtype)
    np.fill_diagonal(L[1:], b)
    np.fill_diagonal(L[:,1:], b)
    return L

def caso_1 (N,dtype): 
    A = generar_matriz(N, dtype)
    t1 = perf_counter()
    result = eigh(A)
    t2 = perf_counter()
    dt = t2-t1
    malloc = A.nbytes + result.__sizeof__()
    return dt, malloc/(10**6)

def caso_2 (N,dtype): 
    A = generar_matriz(N, dtype)
    t1 = perf_counter()
    result = eigh(A,driver="ev",overwrite_a=False)
    t2 = perf_counter()
    dt = t2-t1
    malloc = A.nbytes + result.__sizeof__()
    return dt, malloc/(10**6)

def caso_3 (N,dtype): 
    A = generar_matriz(N, dtype)
    t1 = perf_counter()
    result = eigh(A,driver="ev",overwrite_a=True)
    t2 = perf_counter()
    dt = t2-t1
    malloc = A.nbytes + result.__sizeof__()
    return dt, malloc/(10**6)


def caso_4 (N,dtype): 
    A = generar_matriz(N, dtype)
    t1 = perf_counter()
    result = eigh(A,driver="evd",overwrite_a=False)
    t2 = perf_counter()
    dt = t2-t1
    malloc = A.nbytes + result.__sizeof__()
    return dt, malloc/(10**6)

def caso_5 (N,dtype): 
    A = generar_matriz(N, dtype)
    t1 = perf_counter()
    result = eigh(A,driver="evd",overwrite_a=True)
    t2 = perf_counter()
    dt = t2-t1
    malloc = A.nbytes + result.__sizeof__()
    return dt, malloc/(10**6)


def caso_6 (N,dtype): 
    A = generar_matriz(N, dtype)
    t1 = perf_counter()
    result = eigh(A,driver="evr",overwrite_a=False)
    t2 = perf_counter()
    dt = t2-t1
    malloc = A.nbytes + result.__sizeof__()
    return dt, malloc/(10**6)

def caso_7 (N,dtype): 
    A = generar_matriz(N, dtype)
    t1 = perf_counter()
    result = eigh(A,driver="evr",overwrite_a=True)
    t2 = perf_counter()
    dt = t2-t1
    malloc = A.nbytes + result.__sizeof__()
    return dt, malloc/(10**6)

def caso_8 (N,dtype): 
    A = generar_matriz(N, dtype)
    t1 = perf_counter()
    result = eigh(A,driver="evx",overwrite_a=False)
    t2 = perf_counter()
    dt = t2-t1
    malloc = A.nbytes + result.__sizeof__()
    return dt, malloc/(10**6)

def caso_9 (N,dtype): 
    A = generar_matriz(N, dtype)
    t1 = perf_counter()
    result = eigh(A,driver="evx",overwrite_a=True)
    t2 = perf_counter()
    dt = t2-t1
    malloc = A.nbytes + result.__sizeof__()
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
    output_file.write(f"Corrida B {caso.__name__} {dtype.__name__}:\n")   
    time = [tiempo/10 for tiempo in time]; mem = [memoria/10 for memoria in mem]; Ns = [size/10 for size in Ns]
    for i in range (len(time)):
        output_file.write(f"  {time[i]:.6f}         {mem[i]:.6f}         {int(Ns[i])} \n")
    return 
        
    
    
## MAIN ##
output_file = open("output_file_B_single.txt","w")
output_file.write("Tiempo [segundos] Memoria [MB] Tamaño [N]\n") #header of the txt file

    
    
cases = [caso_1,caso_2,caso_3,caso_4,caso_5,caso_6,caso_7,caso_8,caso_9]
        
        
for casos in cases:
    escribir_corrida(casos, output_file, np.single)

    
    
output_file.write("EOF\n")
output_file.close ()





    