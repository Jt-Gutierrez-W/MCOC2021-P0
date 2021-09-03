# MCOC2021-P0

# Mi computador principal

* Marca/modelo: 
* Tipo: Desktop
* Año adquisición: 2021
* Procesador:
  * Marca/Modelo: Intel Core i5-10400F
  * Velocidad Base: 2.9 GHz
  * Velocidad Máxima: 4.30 GHz
  * Numero de núcleos: 6 
  * Humero de hilos: 12
  * Arquitectura: x86_64
  * Set de instrucciones: Intel SSE4.1, Intel SSE4.2, Intel AVX2
* Tamaño de las cachés del procesador
  * L1d: 384KB
  * L1i: 384KB
  * L2: 1536KB
  * L3: 12288KB
* Memoria 
  * Total: 16 GB
  * Tipo memoria: DDR4
  * Velocidad 3200 MHz
  * Numero de (SO)DIMM: 2
* Tarjeta Gráfica
  * Marca / Modelo: Nvidia GeForce GTX 1660s
  * Memoria dedicada: 5991 MB
  * Resolución: 1920 x 1080
* Disco 1: 
  * Marca: Western Digital
  * Tipo: SSD
  * Tamaño: 0.5TB
  * Particiones: 3
  * Sistema de archivos: NTFS


  
* Dirección MAC de la tarjeta wifi: 18:C0:4D:4B:FB:A7 
* Dirección IP (Interna, del router): 192.168.0.15
* Dirección IP (Externa, del ISP): 190.162.228.140
* Proveedor internet: VTR Banda Ancha S.A.


##### DESEMPEÑO MATMUL #####

1) ¿Cómo difiere del gráfico del profesor/ayudante?

R: Este difiere en los valores particulares de cuanto tarda o cuanta memoria usa para cada corrida en particular. Sin embargo, el comportamiento general del grafico
es el mismo. Con respecto a lo anterior, se puede ver como tiene la misma volatilidad en al zona intermedia para el tiempo. Para la memoria es la misma grafica lineal
con valores particulares distintos.

![](Images/Plot_timing_matmul.png)

2) ¿A qué se pueden deber las diferencias en cada corrida?

R: En el caso del tiempo, las diferencias se deben a los procesos que se estan llevando a cabo en la maquina. El sistema operativo (multi-tasking en este caso), maneja los distintos recursos virtualizandolos y repartiendolos dentro de una cola para cada proceso/programa corriendo en concurrencia (Scheduled Tasks in a Time-Sharing OS). El estado de esta cola es dinamico, por lo que el tiempo en que corre cada programa puede variar por la diferencia de los recursos disponibles y estado de la cola para hacer el "Time-Sharing". Cabe mencionar, que la zona volatil del grafico se debe a los cambios de memoria dependiendo de la jerarquia, por lo que el sistema operativo al ir variando esta, genera algun tipo de volatilidad y mayor tiempo de ejecución.

3) El gráfico de uso de memoria es lineal con el tamaño de matriz, pero el de tiempo transcurrido no lo es ¿porqué puede ser?

R: Esto se debe a la naturaleza del algoritmo. Cada algoritmo tiene una complejidad para la memoria y tiempo, en este caso, matmul simplemente reserva memoria para 3 matrices (cada matriz es una reserva lineal O(N)) por lo que la complejidad para la memoria es O(3N) == O(N). En el tiempo el algoritmo se comporta de forma potencial, ya que la naturaleza de multiplicar matrices implica un ciclo dentro de otro por lo que se comporta potencialmente para el tiempo (probablemente O(N**2)).

4) ¿Qué versión de python está usando?

R: 3.8.5

5) ¿Qué versión de numpy está usando?

R: 1.19.2

6) Durante la ejecución de su código ¿se utiliza más de un procesador? Muestre una imagen (screenshot) de su uso de procesador durante alguna corrida para confirmar. 

R: Durante la ejecución se utilizan los 6 nucleos y 12 threads disponibles (12 procesos). Esto es gracias a la paralelización que facilita numpy.

![](Images/Numero_Procesos_timing_matmul.png)






##### DESEMPEÑO INV #####

1) Comentarios y observaciones:

R: La función inv de numpy no trabaja con float16 y float128, estos tipos de datos no los acepta y por ende no se generaron resultados para esos casos. Cabe mencionar que en los demas casos al trabajar con float128 por lo general este se cambia a float64 ya que python esta codificadao en 64 bits y cualquier valor superior es tomado como si fueran 64 bits. Por otro lado, el float16 en el caso de scipy arroja resultados mas rapidos, es decir al invertir la matriz le toma menos tiempo ya que al utilizar menos bits es mas facil realizar los calculos.

2) ¿Qué algoritmo de inversión cree que utiliza cada método (ver wiki)? Justifique claramente su respuesta. 

R: En el caso de Numpy, este utiliza el algoritmo de factorización LU. Esta consiste en subdividir el problema en problemas vectoriales mas pequeños, siguiendo una logica *"divide and conquer"*. Esto se puede evidenciar en que el comportamiento y complejidad de la función es mas bien del tipo potencial. Lo anterior, calza con el algoritmo para realizar la factorizacion LU, el cual en general es una eliminación Gaussiana o el algoritmo de Doolittle. En ambos casos, es necesario tener "*nested loops*" y por lo tanto su comportamiento es potencial. 
Para el caso de Scipy, tambien utiliza el algoritmo de la factorización LU, esto se puede evidenciar por el comportamiento de la función tal como fue explicado para Numpy. Otra forma de corroborarlo, seria mediante el codigo fuente de Scipy. Al visitarlo en su repositorio en github se puede evidenciar la factorización LU utilizando `getrf` la cual funciona mediante un wrapper de Fortran. 

3) ¿Como incide el paralelismo y la estructura de caché de su procesador en el desempeño en cada caso? Justifique su comentario en base al uso de procesadores y memoria observado durante las corridas. 

R: En general el paralelismo permite la distribucion del trabajo para mejorar el rendimiento y tiempo de ejecucion de los distintos programas. Esta ganancia en eficiencia se debe a que el sistema divide el problema principal en problemas mas pequeños mediante la logica *"divide and conquer"* y estos problemas mas pequeños los distribuye entre los distintos nucleos y threads de la CPU. En cuanto a la estructura del cache, esta al ser una memoria de rapido acceso, permite resolver los problemas mas pequeños (Primeros valores de N) de forma rapida y eficiente a modo de disminuir el tiempo de ejecución. Esto se debe a la jerarquia de las memorias donde la cache es de las mas rapidas pero mas pequeñas al mismo tiempo. En los casos de invertir con numpy se puede apreciar cierta volatilidad en el sector de cambio de jerarquia de memoria por lo que se puede asumir que las funciones de numpy dependen mas de la jerarquia de memoria. Finalmente, en general para datos de menor cantidad de bits existe un mejor desempeño de tiempo, ejecutandose mas rapido el codigo que cuando eran casos de 32 o 64 bits. Esto es bastante esperado ya que a menor cantidad de bits menos calculos y mas rapido se ejecuta el codigo.

Se adjuntan los plots y estado del procesador para cada caso.

Caso 1 Single:

![](Images/Plot_inv_caso1_single.png)

![](Images/timing_inv_caso1_single.png)

Caso 1 Double:

![](Images/Plot_inv_caso1_double.png)

![](Images/timing_inv_caso1_double.png)

Caso 2 Half:

![](Images/Plot_inv_caso2_half.png)

![](Images/timing_inv_caso2_half.png)

Caso 2 Single:

![](Images/Plot_inv_caso2_single.png)

![](Images/timing_inv_caso2_single.png)

Caso 2 Double:

![](Images/Plot_inv_caso2_double.png)

![](Images/timing_inv_caso2_double.png)

Caso 2 Longdouble:

![](Images/Plot_inv_caso2_longdouble.png)

![](Images/timing_inv_caso2_longdouble.png)

Caso 3 Half:

![](Images/Plot_inv_caso3_half.png)

![](Images/timing_inv_caso3_half.png)

Caso 3 Single:

![](Images/Plot_inv_caso3_single.png)

![](Images/timing_inv_caso3_single.png)

Caso 3 Double:

![](Images/Plot_inv_caso3_double.png)

![](Images/timing_inv_caso3_double.png)

Caso 3 Longdouble:

![](Images/Plot_inv_caso3_longdouble.png)

![](Images/timing_inv_caso3_longdouble.png)




##### DESEMPEÑO SOLVE Y EIGH #####



A modo de aclarar a que caso corresponde cada corrida y que parametros incluye, se especifican a continuacion para los distintos items A y B: 

Item A:

Caso 1: A^-1 y luego hacer x= A^-1 * b

Caso 2: scipy.linalg.solve default

Caso 3: scipy.linalg.solve usando assume_a='pos'

Caso 4: scipy.linalg.solve usando assume_a='sym'

Caso 5: scipy.linalg.solve usando overwrite_a=True

Caso 6: scipy.linalg.solve usando overwrite_b=True

Caso 7: scipy.linalg.solve usando overwrite_a=True y overwrite_b=True


Item B:

Caso 1: scipy.linalg.eigh default

Caso 2: scipy.linalg.eigh con driver="ev" y overwrite_a=False

Caso 3: scipy.linalg.eigh con driver="ev" y overwrite_a=True

Caso 4: scipy.linalg.eigh con driver="evd" y overwrite_a=False

Caso 5: scipy.linalg.eigh con driver="evd" y overwrite_a=True

Caso 6: scipy.linalg.eigh con driver="evr" y overwrite_a=False

Caso 7: scipy.linalg.eigh con driver="evr" y overwrite_a=True

Caso 8: scipy.linalg.eigh con driver="evx" y overwrite_a=False

Caso 9: scipy.linalg.eigh con driver="evx" y overwrite_a=True



1) Comentarios y observaciones:

R: En cuanto al item A, se puede observar que resolver el problema invirtiendo y luego multiplicando es bastante caro, por lo que el caso 1 es el de peor rendimiento para casos de N grandes. Sin embargo, para N's pequeños, esta rutina presenta los mejores resultados. Por otro lado, en la medida en que crece el problema el caso 3 presenta los mejores resultados demorandose el menor tiempo y utilizando la misma cantidad de memoria. En cuanto a la memoria, el caso 1 es el que mas utiliza, por lo que no seria recomendable aplicar esta rutina en casos donde la memoria se vea limitada. En cuanto al tipo de dato, se puede apreciar que el dato double en general tarda un poco mas en procesar y entregar resultados para Ns grandes. 

En cuanto al item B, el comportamiento es más homogeneo con una leve superioridad del caso 5 y caso 4 los cuales demuestran una leve mejoria en el tiempo de ejecución. En cuanto a la memoria, se puede observar que se comporta de forma lineal para ambos tipos de datos, con un leve aumento en el tipo double por razones obvias. Dentro de esta grafica lineal, se puede observar un pequeño comportamiento potencial al principio del grafico, probablemente por el over-head que necesita dicha funcion o rutina para correr. Finalmente, en el caso de dato single, se puede ver una mayor volatilidad en la zona inicial del grafico de tiempo, probablemente por el over-head y jerarquia de la memoria.

2) ¿Como es la variabilidad del tiempo de ejecucion para cada algoritmo?

R: Para el item B, se puede apreciar que en general el comportamiento es parecido para todos los casos probados, sin embargo, existe una leve mejora para el caso 4 y caso 5. Probablemente tenga que ver con los driver los cuales componen cierta rutina que determina la estrategia o forma para resolver el problema. Estas rutinas pueden ser estudiadas en la documentación de LAPACK.

Para el item A, el comportamiento tambien es bastante parecido con algunas diferencias en casos especificos como el caso 1 el cual invierte la matriz y luego multiplica. Los demas casos tienden a comportarse de forma similar con una leve mejoria del caso 3 el cual presenta el menor tiempo de ejecución. En cuanto a la zona inicial de Ns pequeños existe mayor volatilidad en el tiempo de ejecución, pero luego tienden a unificarse y comportarse de manera similar. Finalmente, en ambos tipos de datos el comportamiento es similar.

3) ¿Qué algoritmo gana (en promedio) en cada caso?

R: En el item A gana el caso 3 para ambos tipos de datos, assumiendo la matriz como definida postivia (assume_a='pos').
En el item B, gana el caso 4 y caso 5 para ambos tipos de datos, por lo que para mi sistema el driver 'evd' presenta la mejor rutina.

4) ¿Depende del tamaño de la matriz?

R: Si, por ejemplo, en el item A, el caso 1 es el mejor metodo para tamaños de matriz pequeños, pero a medida que aumenta el tamaño este algortimo presenta bastantes falencias.

5) ¿A que se puede deber la superioridad de cada opción?

R: Al algoritmo y compatibilidad con el sistema, distintos algoritmos pueden estar basados en distintos metodos que consuman mas memoria para mejorar el tiempo de ejecución o viceversa, dependiendo de las especificaciones del sistema si se tiene buena CPU o mucha memoria un metodo u otro puede ser mejor o peor. Ejemplos de algoritmos que priorizan tiempo por sobre memoria es utilizar programación dinámica. 

6) ¿Su computador usa más de un proceso por cada corrida?

R: Si, para todos los casos la maquina se aprovecha del paralelismo a modo de mejorar el tiempo de ejecución. Para esto distribuye el prolema grande en sub-problemas, los cuales distribuye en los distintos nucleos y threads. Se adjuntan imagenes del procesador para cada corrida.

Item_A_Single:

![](Entrega4/Item_A_single_cpu.png)

Item_A_Double:

![](Entrega4/Item_A_double_cpu.png)

Item_B_Single:

![](Entrega4/Item_B_single_cpu.png)

Item_B_Double:

![](Entrega4/item_B_double_cpu.png)



7) ¿Que hay del uso de memoria (como crece)? 

R: En general el uso de memoria de comporta de forma lineal con una pequeña variacion al inicio de los Item_B. Esto era de esperar ya que en general la memoria que reserva es la correspondiente a las multiples matrices para realizar el algoritmo y resolver el problema.

Item_A_Single:

![](Entrega4/Item_A_single_mem.png)

Item_A_Double:

![](Entrega4/Item_A_double_mem.png)

Item_B_Single:

![](Entrega4/Item_B_single_mem.png)

Item_B_Double:

![](Entrega4/Item_B_double_mem.png)




##### MATRICES DISPERSAS Y COMPLEJIDAD COMPUTACIONAL #####


1) Comentarios y observaciones:

R: En cuanto al codigo de ensamblaje, se aprovechó la eficiencia de la libreria numpy para generar estas matrices, ya que, al estar programada en C y Fortran presenta grandes ganancias en tiempo de ejecución por la naturaleza del bajo nivel. Ademas, estas librerias presentan algoritmos optimizados para funcionar en python y minimizar el tiempo de las corridas. Al mismo tiempo, en base a los graficos obtenidos, se puede ver que la complejidad para ensamblaje es lineal, lo cual es bastante bueno en el mercado, ya que esta complejidad es muy valorada en el mercado de la ingenieria de software al comportarse de buena forma frente a N's muy grandes. En cuanto a la solución (Matmul), se puede apreciar que es de caracter cubica asintoticamente. Este tipo de complejidad no es la mejor del mundo, sin embargo, por la naturaleza del problema de multiplicar matrices no debe ser posible alcanzar una complejidad menor y esta complejidad cubica debe ser la mejor y más optimizada. Finalmente, al comparar el caso sparse y llena, la matriz sparse presenta mejorar en el tiempo de ejecución, al optimizar el uso de memoria y de esta forma el calculo, sin embargo, ambos tipos de matriz presentan la misma complejidad para el codigo.


Codigo de ensamblaje matriz llena:

```
def generar_matriz_llena (N,dtype): 
    t1 = perf_counter()  
    L=np.zeros((N,N),dtype=dtype)
    np.fill_diagonal(L, dtype(2))
    np.fill_diagonal(L[1:], -np.ones(N-1,dtype=dtype))
    np.fill_diagonal(L[:,1:], -np.ones(N-1,dtype=dtype))
    t2 = perf_counter()
    dt = t2-t1
    return L, dt   
```
Codigo de ensamblaje matriz sparse:

```
def generar_matriz_sparse(N,dtype):
    t1 = perf_counter()
    L = csr_matrix((N,N),dtype=dtype).toarray()
    np.fill_diagonal(L, dtype(2))
    np.fill_diagonal(L[1:], -np.ones(N-1,dtype=dtype))
    np.fill_diagonal(L[:,1:], -np.ones(N-1,dtype=dtype))
    t2 = perf_counter()
    dt = t2-t1
    return L, dt  

```

Rendimiento matmul matriz llena:

![](Images/timing_matmul_llena.png)

Rendimiento matmul matriz sparse:

![](Images/timing_matmul_sparse.png)







##### MATRICES DISPERSAS Y COMPLEJIDAD COMPUTACIONAL (PARTE 2) #####


1) Comentarios y observaciones:

R: Para el caso de solve, se puede ver que al utilizar matrices sparse, el tiempo de resolución y complejidad del algoritmo son mucho menores que en el formato de matriz llena. Esta ganancia en tiempo, se debe a que la matriz sparse utiliza menos memoria, ya que, los ceros no son tomados en cuenta y solo se guardan los valores numericos distintos de cero. Para implementar esto, los valores distintos de cero, son almacenados en un array por posición de filas o columnas y con los valores uno al lado de otro en orden creciente. Gracias a esto, la matriz pasa de ser un elemento "uni-dimensional" ayudando a bajar la complejidad de los algoritmos asociados a esta, ya que, en vez de recorrer toda la matriz, simplemente se recorren estos elementos no nulos, ayudando asi a eliminar los "nested loops" y mejorando el algoritmo solver.
Lo anterior, se puede apreciar en los graficos generados, ya que la complejidad para el caso sparse es O(N) y para el caso llena es O(N^3).
Cabe mencionar, que el ensamblaje se mantiene como complejidad lineal, sin embargo, al resolver tan rapido los primeros 20000 casos se presenta al principio como un comportamiento constante, sin embargo, alfinal se aprecia su verdadera forma O(N).

Para el caso de inv, la diferencia no es tan significativa como en el caso de solve, aun asi se puede apreciar una ganancia en complejidad por lo anteriormente mencionado. En el caso sparse, se puede apreciar como se comporta de forma potencial menor o igual a O(N^3) dependiendo del sector que se analice, mientras que en el caso llena se comporta de forma cubica desde mucho antes, tomandole mas tiempo de solución en los casos donde N es mas grande. Cabe mencionar, que para inputs pequeños el caso lleno se comporta mejor, lo cual es bastante esperado, ya que los algoritmos para invertir matrices sparse son mas complejos y requieren mas pasos (para aprovechar los valores nulos).


2) ¿Cual parece la complejidad asintótica (para N→∞) para el ensamblado y solución en ambos casos y porqué?

R: Para el caso de solve, el ensamblaje en ambos casos se comporta de forma lineal, sin embargo, en el caso sparse, al tener que guardar menos valores, se ve un especie de comportamiento constante, ya que, aun no llega al sector lineal por la pequeña cantidad de valores que debe guardar (solo guarda en memoria los valores no nulos), entonces alfinal esta curva se desplaza hacia la derecha. El comportamiento lineal, se debe a que se requiere solo un loop para recorrer todos los valores que deben ir en la matriz, si este loop es muy pequeño el comportamiento se puede aproximar a constante que es lo que se observa en el caso sparse.
Para la solución, el comportamiento sparse es lineal, lo cual se debe a que al tener menos valores asociados a la matriz, "baja" la dimension de esta y requiere menos loops para recorrer y resolver el problema en si. Cabe mencionar, que el metodo que usa para resolver el problema es una factorización LU y luego con estas aplciar operaciones de fila y dividir el problema grande en problemas mas pequeños, al tener "menos dimensiones" en el problema se requieren menos loops y de esta forma baja la complejidad. En el caso de  llena, el comportamiento es cubico asintoticamente, por la cantidad de loops que significa la descomposición LU, en este caso no existe una baja de dimension ya que todos los valores son guardados en memoria de la misma manera.

Para el caso inv, en el ensamblaje pasa exactamente lo mismo que en el caso de solve. 
Para la solución, la complejidad sparse tiende a ser O(N^2) en la mitad y luego asintoticamente O(N^3), al invertir matrices no es de mucha ayuda que sea sparse ya que al invertir, hay que realizar operacioens de fila y luego guardarlas en otra matriz que sera la resultante, por esto, en el proceso se puede perder la matriz sparse y terminar guardando todos los valores culminando en una matriz llena. Cabe mencionar, que invertir es un proceso muy caro, por lo que aun cuando se tiene una matriz sparse no conviene invertir ya que se pierde este beneficio.

3) ¿Como afecta el tamaño de las matrices al comportamiento aparente?

R: Esta afecta de gran forma, ya que dependiendo del tamaño del input la función (solve o inv) se comporta de distinta forma. Esto se debe a que, aun cuando se tiene un codigo potencial, en algunos casos si el input es muy pequeño los loops ocurren muy pocsa veces "mostrando" una complejidad menor a la que enverdad se tiene. Por esto, ante distintos tamaños de inputs existen distintos comportamientos. Por ejemplo, en inversa sparse, en tamaños de N medianos el comportamiento se asemeja a una función cuadratica, pero al llegar al N mas grande, se comporta de forma cubica. Otro ejemplo es el ensamblaje, donde para N pequeños el comportamiento es del tipo constante. Finalmente, esto ayuda a elegir de que forma resolver el problema, ya que aveces el sparse no es lo mejor, ya que si mi problema es acotado, incluso utilizar el formato llena puede ser mejor para N's pequeños.

4) ¿Qué tan estables son las corridas (se parecen todas entre si siempre, nunca, en un rango)?

R: En general para el tipo de matriz sparse en ambas funciones las corridas son bastante estables, manteniendose de forma homogenea en el mismo rango, por lo que se puede asumir que en el caso sparse, al trabajar los datos, se utilizan algoritmos que dependen menos del estado de la maquina (Scheduled tasks in the OS) y mas del codigo en si, ayudando a mantener todas las corridas en rangos muy similares. Esto, se puede explicar gracias al ahorro de calculos en una matriz sparse, lo que genera menos dependencia de los recursos virtualizados. Al mismo tiempo, las rutinas que involucran operaciones de fila y columna son mas compactas ayudando a reducir la volatilidad.
En el caso de matriz llena, existe mucha mayor volatilidad, debido a que no cuentan con el ahorro de memoria que si tiene el caso sparse, en el caso de matriz llena, al tener que realizar todas las operaciones, incluidas las colocaciones de ceros, se tienen bastantes operaciones en paralelo, teniendo que asignar direcciones y lugares de memoria para muchos datos al mismo tiempo, de cierta forma "saturando" los recursos generando ciertas volatilidades en algunas corridas. Cabe mencionar, que dependiendo del rango existe mayor o menor volatilidad, por ejemplo, al principio para N's pequeños, hay mayor volatilidad, ya que el overhead toma mas peso para el tiempo de solución, sin embargo, en el final de las corridas el overhead es muy chico en comparación a la resolución del problema en si, por lo que las corridas son mas estables y parecidas entre cada una.

Codigo de ensamblaje:

```
def generar_matriz_llena (N,dtype): 
    t1 = perf_counter()  
    L=np.zeros((N,N),dtype=dtype)
    np.fill_diagonal(L, dtype(2))
    np.fill_diagonal(L[1:], -np.ones(N-1,dtype=dtype))
    np.fill_diagonal(L[:,1:], -np.ones(N-1,dtype=dtype))
    t2 = perf_counter()
    dt = t2-t1
    return L, dt   
```
```
def generar_matriz_sparse(N,dtype): 
    t1 = perf_counter()
    L = diags([-1, 2, -1], [-1, 0, 1], shape=(N, N)) 
    t2 = perf_counter()
    dt = t2-t1
    return L, dt  
```

Se adjuntan los graficos correspondientes a cada caso:

Solve Sparse:

![](Images/plot_solve_sparse.png)

Solve Llena:

![](Images/plot_solve_llena.png)

Inv Sparse:

![](Images/plot_inv_sparse.png)

Inv Llena:

![](Images/plot_inv_llena.png)
