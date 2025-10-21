#!/usr/bin/env python3
import os, sys, re

#Comprobamos argumentos
if len(sys.argv) != 3:
    print("Uso: ./gen-1.py <fichero-entrada> <fichero-salida>")
    sys.exit(1)

fichero_entrada = sys.argv[1]   # fichero de entrada
fichero_salida_dat = sys.argv[2]  # fichero de sal
fichero_salida_sol = "parte-2/solucion221.txt"
fichero_salida_compl = "parte-2/salida_completa221.txt"  # captura toda la salida

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

# Ejecutamos GLPK (redirigiendo toda la salida para en pantalla poder imprimir lo que nos obliga el enunciado)
comando = f'glpsol --model parte-2\\minperdidas.mod --data "{fichero_salida_dat}" -o "{fichero_salida_sol}" > "{fichero_salida_compl}"'
os.system(comando)

print("GLPK ejecutado correctamente")

#
Z = rows = cols = None
asignaciones = []
no_asignados = []

#Leemos la salida estándar y mostramos por pantalla loque nos piden en el enunciado ---
if os.path.exists(fichero_salida_sol):
    with open(fichero_salida_sol, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            # Extraer los datos
            if line.startswith("Objective:"):
                m = re.search(r"=\s*([\d\.]+)", line)
                if m: Z = float(m.group(1))
            elif line.startswith("Rows:"):
                m = re.search(r"(\d+)", line)
                if m: rows = int(m.group(1))
            elif line.startswith("Columns:"):
                m = re.search(r"(\d+)", line)
                if m: cols = int(m.group(1))

            # Extraer asignaciones
            m_x = re.match(r".*x\[(\w+),(\w+)\]\s+\*?\s*(\d+)", line)
            if m_x and m_x.group(3) == "1":
                asignaciones.append((m_x.group(1), m_x.group(2)))

            m_a = re.match(r".*a\[(\w+)\]\s+\*?\s*(\d+)", line)
            if m_a and m_a.group(2) == "1":
                no_asignados.append(m_a.group(1))

#Mostramos los resultados
print(f"Z* = {Z if Z is not None else 'NA'} , variables = {cols if cols is not None else 'NA'} , restricciones = {rows if rows is not None else 'NA'}")

#Buses asignados
print("\nAsignaciones\n")
for bus, franja in asignaciones:
    print(f"{bus} → {franja}")

for bus in no_asignados:
    print(f"{bus} → sin asignar")