#!/usr/bin/env python3
import os, sys

#Comprobamos argumentos
if len(sys.argv) != 3:
    print("Uso: ./gen-1.py <fichero-entrada> <fichero-salida>")
    sys.exit(1)

fichero_entrada = sys.argv[1]   # fichero de entrada
fichero_salida_dat = sys.argv[2]  # fichero de sal
fichero_salida_sol = "solucion221.txt"
fichero_salida_compl = "salida_completa221.txt"  # captura toda la salida

# Leemos el fichero de entrada (texto plano)
lineas = []
with open(fichero_entrada, "r", encoding="utf-8") as f:
    for linea in f:
        linea = linea.strip()
        if linea != "":
            lineas.append(linea)

# Procesamos las líneas según el formato del enunciado
primera = lineas[0].split()
n = int(primera[0])   # número de franjas
m = int(primera[1])   # número de autobuses

segunda = lineas[1].split()
kd = float(segunda[0])  # euros/km
kp = float(segunda[1])  # penalización/pasajero

tercera = lineas[2].split()
d = []
for valor in tercera:
    d.append(float(valor))

cuarta = lineas[3].split()
p = []
for valor in cuarta:
    p.append(float(valor))

#Creamos listas de nombres de autobuses y franjas
autobuses = []
for i in range(m):
    autobuses.append("a" + str(i + 1))

franjas = []
for j in range(n):
    franjas.append("s" + str(j + 1))

#Creamos el texto que se encontrara dentro de nuestro .dat
texto = ""
texto += "data;\n\n"
texto += "set AUT := " + " ".join(autobuses) + ";\n\n"
texto += "set FRAN := " + " ".join(franjas) + ";\n\n"

# kd y kp son constantes globales
texto += "param kd := " + str(kd) + ";\n"
texto += "param kp := " + str(kp) + ";\n\n"

# Distancias
texto += "param DIST :=\n"
for i in range(m):
    texto += autobuses[i] + " " + str(d[i]) + "\n"
texto += ";\n\n"

# Pasajeros
texto += "param PAS :=\n"
for i in range(m):
    texto += autobuses[i] + " " + str(p[i]) + "\n"
texto += ";\n\n"

texto += "end;\n"

# Guardamos el .dat
with open(fichero_salida_dat, "w", encoding="utf-8") as f:
    f.write(texto)

print("Generado " + fichero_salida_dat + " correctamente")

# Ejecutamos GLPK (redirigiendo toda la salida)
comando = f'glpsol --model 2.2.1\\minperdidas.mod --data "{fichero_salida_dat}" -o "{fichero_salida_sol}" > "{fichero_salida_compl}"'
os.system(comando)

print("GLPK ejecutado correctamente")

# Leemos la salida completa
Z = None
rows = None
cols = None
lineas = []

if os.path.exists(fichero_salida_sol):
    with open(fichero_salida_sol, "r", encoding="utf-8", errors="ignore") as f:
        for fila in f:
            s = fila.strip()
            if s.startswith("Objective:"):
                try:
                    Z = float(s.split('=')[1].split()[0])
                except:
                    pass
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

if os.path.exists(fichero_salida_compl):
    with open(fichero_salida_compl, "r", encoding="utf-8", errors="ignore") as f:
        for fila in f:
            s = fila.strip()
            if s.startswith("Bus "):
                lineas.append(s)

# Mostramos resultados
print("Z* =", Z if Z is not None else "NA",
      ", variables =", cols if cols is not None else "NA",
      ", restricciones =", rows if rows is not None else "NA")

for l in lineas:
    print(l)