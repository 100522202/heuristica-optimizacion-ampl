#!env python
import os, sys, re

#Comprobamos argumentos
if len(sys.argv) != 3:
    print("Uso: ./gen-1.py <fichero-entrada> <fichero-datos>")
    sys.exit(1)

fichero_entrada = sys.argv[1]   # fichero de entrada
fichero_salida_dat = sys.argv[2]  # fichero .dat
fichero_salida_sol = "parte-2/solucion222.txt"
fichero_salida_compl = "parte-2/salida_completa222.txt"  # captura toda la salida

# Leemos el fichero de entrada que está en texto plano
#Eliminamos huecos en blanco si los hubiera
lineas = []
with open(fichero_entrada, "r", encoding="utf-8") as f:
    for linea in f:
        linea = linea.strip()
        if linea != "":
            lineas.append(linea)


#Procesamos las lineas según el formato del enunciado
primera = lineas[0].split()
f = int(primera[0]) #Número de franjas
a = int(primera[1]) #Número de autobuses
t = int(primera[2]) #Núemro de talleres

cij = [] #Inizializmaos la matriz que va a contener los pasajeros compartidos 

for i in range(1, a + 1): #Empezamos en la segunda fila 
    texto = lineas[i].split() #Divido la linea en valores separados por espacio
    numeros_fila = []

    for text in texto:
        numeros_fila.append(int(text)) #Los agrego a la matriz transformados a entero

    cij.append(numeros_fila) #Agregamos la fila a la matriz

oij = [] #Matriz que contendra cada taller por fila con la disponibilidad de su franja
# sera 1 si está disponible 0 si no lo está

for i in range(a + 1, a + f + 1):
    texto = lineas[i].split()  #Divido la linea en valores separados por espacio
    numeros_fila = []

    for text in texto:
        numeros_fila.append(int(text)) #Los agrego a la matriz transformados a entero

    oij.append(numeros_fila) #Agregamos la fila a la matriz

#Creamos listasde nombres de autobuses, franjas y talleres
autobuses = []
for i in range(a):
    autobuses.append("a" + str(i+1))

franjas = []
for j in range(f):
    franjas.append("s" + str(j + 1))

talleres = []
for k in range(t):
    talleres.append("t" + str(k + 1))


#Creación del archivo .dat

#Creamos el texto que se encontrará dentro de nuestro .dat
texto = ""
texto += "data;\n\n"
texto += "set AUT := " + " ".join(autobuses) + ";\n\n"
texto += "set TALL := " + " ".join(talleres) + ";\n\n"
texto += "set FRAN := " + " ".join(franjas) + ";\n\n"

# CIJ y OIJ son constantes globales

#CIJ
texto += "param CIJ : " + " ".join(autobuses) + " :=\n"
for i in range(a):
    linea = autobuses[i] + " " #Creamos la linea con el nombre de la fila
    for j in range(a):
        linea += str(cij[i][j]) + " "
    texto += " " + linea +"\n"
texto += ";\n\n"


#OIJ
texto += "param OIJ : " + " ".join(talleres) + " :=\n"
for i in range(f):
    linea = franjas[i] + " " #Creamos la linea con el nombre de la fila
    for j in range(t):
        linea += str(oij[i][j]) + " "
    texto += " " + linea +"\n"
texto += ";\n\n"
texto += "end;\n"

#Guardamos en el .dat
with open(fichero_salida_dat, "w", encoding="utf-8") as f:
    f.write(texto)


# Ejecutamos GLPK (redirigiendo toda la salida para en pantalla poder imprimir lo que nos obliga el enunciado)
comando = f'glpsol --model parte-2\\parte-2-2.mod --data "{fichero_salida_dat}" -o "{fichero_salida_sol}" > "{fichero_salida_compl}"'
os.system(comando)

print("GLPK ejecutado correctamente")

Z = None                # valor de la función objetivo
rows = None             # número de restricciones
cols = None             # número de variables
asignaciones = []       # lista de tuplas con las asignaciones encontradas
status = None           # estado del modelo (OPTIMAL, INFEASIBLE, etc.)
infeasible = False      # indicador de si el modelo es infactible

#Comprobamos que existe el fichero de la solución
if os.path.exists(fichero_salida_sol):
    #Abrimos el archivo para leerlo
    with open(fichero_salida_sol, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip() #Quitamos espacios si lo shubiera

            # Detectar si el modelo es factible
            if line.startswith("Status:"):
                status = line.split(":")[1].strip().upper()
                if "INFEASIBLE" in status or "INTEGER EMPTY" in status:
                    infeasible = True
            
            #Por si aparece en otra linae
            elif "INTEGER EMPTY" in line.upper() or "INFEASIBLE" in line.upper():
                infeasible = True

            #Detectamos el valor de la función objetivo 
            elif line.startswith("Objective:"):
                partes = line.split("=")
                if len(partes) > 1:
                    try:
                        Z = float(partes[1].split()[0])  # primer número después de "="
                    except:
                        Z = None
        
            #Determinamos el número de restricciones creadas (rows)
            elif line.startswith("Rows:"):
                partes = line.split()
                if len(partes) > 1:
                    try:
                        rows = int(partes[1])
                    except:
                        rows = None

            #Recopilamos el número de variables credas (columns)
            elif line.startswith("Columns:"):
                partes = line.split()
                if len(partes) > 1:
                    try:
                        cols = int(partes[1])
                    except:
                        cols = None

            # Asignaciones x[a,t,f] = 1
            x_a_t_f = re.match(r".*x\[(\w+),(\w+),(\w+)\]\s+\*?\s*(\d+)", line)
            if x_a_t_f and x_a_t_f.group(4) == "1": #Grupo 4 es la Columna de Activity en la solución
                asignaciones.append((x_a_t_f.group(1), x_a_t_f.group(2), x_a_t_f.group(3)))
                
    
#Mostrmos los resultados por pantalla
if infeasible:
    print("\nEl modelo es infactible, no existen asignaciones válidas ")
else:
    print(f"\nZ* = {Z if Z is not None else 'NA'} , variables = {cols if cols is not None else 'NA'} , restricciones = {rows if rows is not None else 'NA'}\n")
    print("Asignaciones óptimas:\n")
   
    if len(asignaciones) > 0:
       for asignacion in asignaciones:
           a = asignacion[0]
           t = asignacion[1]
           f = asignacion[2]
           print(a, "asignado a", t, ",", f)
