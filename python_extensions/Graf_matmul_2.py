import matplotlib.pyplot as plt


import numpy as np

time_E = []; size = []; time_M = [];
time_E_buffer = []; size_buffer = []; time_M_buffer = [];
file = open("output_file_timing_matmul_llena.txt","r")
lineas=file.readlines()
for linea in lineas:
    buffer =list(linea.split())
    
    if len(buffer) == 6:
        pass
    if (len(buffer) == 2 and buffer[1] != '1' and len(time_E_buffer)!=0) or buffer[0] == "EOF":
        
        time_E.append(time_E_buffer); size.append(size_buffer); time_M.append(time_M_buffer);
        time_M_buffer = []; size_buffer = []; time_E_buffer = []
    if len (buffer) == 3:
        time_E_buffer.append(float(buffer[0])); time_M_buffer.append(float(buffer[1])); size_buffer.append(float(buffer[2]))
        

        
x = [10,20,50,100,200,500,1000,2000,5000,10000,20000]
y_time = [1e-4, 0.001, 0.01, 0.1, 1, 10, 60, 600] #ticks
y_labels = ["0.1 ms", "1 ms", "10 ms", "0.1 s", "1 s", "10 s", "1 min", "10 min"]
y_memory = [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
y_mlabels = ["1 KB", "10 KB", "100 KB", "1 MB", "10 MB", "100 MB", "1 GB", "10 GB"]



plt.figure(1,figsize=(9,9))

plt.subplot(2,1,1)
plt.title("Rendimiento A@B")
plt.ylabel("Tiempo de ensamblado (s)")
mean_e=0
for run in time_E:
    plt.loglog(size[0],run,color='gray',zorder=1)
    plt.scatter(size[0],run,color='black',zorder=2)
    mean_e+= run[-1]

mean_e*=0.1

N=np.array(size[0])
plt.loglog(N,[mean_e]*len(N),'--', color = 'blue',label="O(C)")
plt.loglog(N,(mean_e/N[-1])*(N),'--', color = 'orange',label="O(N^1)")
plt.loglog(N,(mean_e/N[-1]**2)*(N**2),'--', color = 'green',label="O(N^2)")
plt.loglog(N,(mean_e/N[-1]**3)*(N**3),'--', color = 'red',label="O(N^3)")
plt.loglog(N,(mean_e/N[-1]**4)*(N**4),'--', color = 'pink',label="O(N^4)")
plt.ylim(0.000001,500)

plt.yticks(y_time, y_labels)
plt.xticks(x,[],rotation = 70)
plt.grid()




plt.subplot(2,1,2)
plt.xlabel("Tamaño matriz N")
plt.ylabel("Tiempo de solucion (s)")

mean_e=0

for corun in time_M:
    plt.loglog(size[0],corun,color='gray',zorder=1)
    plt.scatter(size[0],corun,color='black',zorder=2)
    mean_e+=corun[-1]

mean_e*=0.1

N=np.array(size[0])
plt.loglog(N,[mean_e]*len(N),'--', color = 'blue',label="O(C)")
plt.loglog(N,(mean_e/N[-1])*(N),'--', color = 'orange',label="O(N^1)")
plt.loglog(N,(mean_e/N[-1]**2)*(N**2),'--', color = 'green',label="O(N^2)")
plt.loglog(N,(mean_e/N[-1]**3)*(N**3),'--', color = 'red',label="O(N^3)")
plt.loglog(N,(mean_e/N[-1]**4)*(N**4),'--', color = 'magenta',label="O(N^4)")
plt.ylim(0.000001,600)

plt.legend(prop={'size': 13})
plt.yticks(y_time, y_labels)
plt.xticks(x,x,rotation = 70)
plt.grid()



plt.show()
file.close()