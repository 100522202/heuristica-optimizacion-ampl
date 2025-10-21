#!/usr/bin/env python3
import json, os, sys

#Comprobamos argumentos
if len(sys.argv) != 3:
    print("Uso: ./gen-1.py <fichero-entrada> <fichero-salida>")
    sys.exit(1)

fichero_entrada = sys.argv[1]   # json dentro de .in
fichero_salida_dat = sys.argv[2]  # .dat a generar
fichero_salida_sol = "salida_completa221.txt"  # capturará toda la salida de GLPK (solver + printf del modelo)

#Abrimos el archivo json donde se encuentran los datos
with open(fichero_entrada, "r", encoding="utf-8") as f:
    datos = json.load(f) #Cargamos el json donde están los datos

autobuses = datos["AUT"] #Obtenemos los datos de los autobuses y devuelve la lista correspondiente
franjas = datos["FRAN"] #Obtenemos los datos de las franjas de talleres y  devuelve la lista correspondiente
euros = datos["EUR"] #Obtenemos el coste  eur/km y devuelve la lista correspondiente
penalizacion = datos["PEN"] #Obtenemos la penalización por pasajero y  devuelve la lista correspondiente
pasajeros = datos["PAS"] #Obtenemos la cantidad de pasajeros en cada autobus
dist = datos["DIST"] #Obtenemos la distancia entre cada autobus y franja y  devuelve la lista correspondiente

#Creamos el texto que se encontrara dentro de nuestro .dat
texto = ""
texto += "data;\n\n" #Añaidmos esto al prinicipio del fichero
texto += "set AUT := " + " ".join(autobuses) + ";\n\n" # Añadimos a set AUT la lista de autobuses obtenida anteriormente del json
texto += "set FRAN := " + " ".join(franjas) + ";\n\n"  # Añadimos a set TALL la lista de franjas obtenida anteriormente del json

#Rellenamos la matriz que representa el coste eur/km
texto += "param EUR :=\n"
for bus in autobuses:
    linea = bus + " " + str(euros[bus]) + "\n"
    texto += linea
texto += ";\n\n"

#rellenamos la matriz que representa las penalizaciones por cliente de cada bus
texto += "param PEN :=\n"
for bus in autobuses:
    linea = bus + " " + str(penalizacion[bus]) + "\n"
    texto += linea
texto += ";\n\n"

#Rellenamos la matriz que representa las cantidad de pasajeros por autobús
texto += "param PAS :=\n"
for bus in autobuses:
    linea = bus + " " + str(pasajeros[bus]) + "\n"
    texto += linea
texto += ";\n\n"

#Rellenamos la matriz que representa las distanias entre autobuses y franjas
texto += "param DIST : " + " ".join(franjas) + " :=\n"
for bus in autobuses:
    linea = bus + " "
    for fran in franjas:
        linea += str(dist[bus][fran]) + " "
    texto += "  " + linea + "\n"
#Indidcamos el final con un ;
texto += ";\n\nend;\n" #Añado un end al final del fichero

#Abrimos un archivo .dat (segundo argumento) en el cual escribiremos el texto
#generado en la variable anterior
with open(fichero_salida_dat, "w", encoding="utf-8") as f:
    f.write(texto)

print(f"Generado {fichero_salida_dat} correctamente")

#Resuelve el glpk con os.system que es similar a escribir en la terminal el
# contenido descrito en la variable "comando"
# Redirigimos toda la salida a 'salida_completa.txt' para capturar también los printf del modelo
comando = f'glpsol --model 2.2.1\\minperdidas.mod --data "{fichero_salida_dat}" -o "solucion221.txt" > "{fichero_salida_sol}"'
os.system(comando)

print("GLPK ejecutado correctamente")

# Leemos la salida completa (solver + printf del modelo)
Z = None
rows = None
cols = None
lineas = []

if os.path.exists(fichero_salida_sol):
    with open(fichero_salida_sol, "r", encoding="utf-8", errors="ignore") as f:
        for fila in f:
            s = fila.strip()
            # Buscar el valor óptimo de la función objetivo
            if s.startswith("Objective:"):
                try:
                    Z = float(s.split('=')[1].split()[0])
                except:
                    pass
            # Buscar número de restricciones y variables
            if s.startswith("Rows:"):
                try:
                    rows = int(s.split()[1])
                except:
                    pass
            if s.startswith("Columns:"):
                try:
                    cols = int(s.split()[1])
                except:
                    pass
            # Buscar las líneas de salida del modelo (Bus ...)
            if s.startswith("Bus "):
                lineas.append(s)

# Primera línea con Z*, nº de variables y nº de restricciones
print(f"Z* = {Z if Z is not None else 'NA'} , variables = {cols if cols is not None else 'NA'} , restricciones = {rows if rows is not None else 'NA'}")

# Luego, las líneas de solución legibles
for l in lineas:
    print(l)
