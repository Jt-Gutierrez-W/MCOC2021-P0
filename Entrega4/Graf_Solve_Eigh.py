
import matplotlib.pyplot as plt


time = []; size = []; memory = [];
time_buffer = []; size_buffer = []; memory_buffer = [];
file = open("output_file_A_single.txt","r") #reemplazar nombre del archivo y Title para generar nuevo grafico
lineas=file.readlines()
for linea in lineas:
    buffer =list(linea.split())
    
    if len(buffer) == 6:
        pass
    if (len(buffer) == 4 and buffer[2] != 'caso_1' and len(time_buffer)!=0) or buffer[0] == "EOF":
        
        time.append(time_buffer); size.append(size_buffer); memory.append(memory_buffer);
        memory_buffer = []; size_buffer = []; time_buffer = []
    if len (buffer) == 3:
        time_buffer.append(float(buffer[0])); memory_buffer.append(float(buffer[1])); size_buffer.append(float(buffer[2]))
        

        
colors = ['b','#347235','#DC143C','c','m','orange','#00FF00','black','pink']
x = [10,20,50,100,200,500,1000,2000,5000,10000]
y_time = [1e-4, 0.001, 0.01, 0.1, 1, 10, 60, 600] #ticks
y_labels = ["0.1 ms", "1 ms", "10 ms", "0.1 s", "1 s", "10 s", "1 min", "10 min"]
y_memory = [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
y_mlabels = ["1 KB", "10 KB", "100 KB", "1 MB", "10 MB", "100 MB", "1 GB", "10 GB"]

plt.figure(1,figsize=(7,7))



plt.title("Item_A_single")
plt.ylabel("Tiempo transcurrido (s)")
for numero,run in enumerate(time,start=1):
    plt.loglog(size[0],run)
    plt.plot(size[0],run,color=colors[numero-1],marker='o',label=f"caso_{numero}")
    plt.legend()
plt.yticks(y_time, y_labels)
plt.xticks(x,x,rotation = 70)
plt.grid()




plt.figure(2,figsize=(7,7))
plt.xlabel("Tamaño matriz N")
plt.ylabel("Uso memoria (s)")
plt.axhline(y=16000, color='black', linestyle='--')
plt.title("Item_A_single")


for numero,corun in enumerate(memory,start=1):
    plt.loglog(size[0],corun)
    plt.plot(size[0],corun,color=colors[numero-1],marker='o',label=f"caso_{numero}")
    plt.legend()
plt.yticks(y_memory,y_mlabels)
plt.xticks(x,x,rotation = 70)
plt.grid()



plt.show()
file.close()