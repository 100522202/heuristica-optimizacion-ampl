import os, sys, re

#Comprobamos argumentos
if len(sys.argv) != 3:
    print("Uso: ./gen-1.py <fichero-entrada> <fichero-datos>")
    sys.exit(1)

fichero_entrada = sys.argv[1]   # fichero de entrada
fichero_salida_dat = sys.argv[2]  # fichero .dat
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
comando = f'glpsol --model parte-2\\parte-2-1.mod --data "{fichero_salida_dat}" -o "{fichero_salida_sol}" > "{fichero_salida_compl}"'
os.system(comando)

print("GLPK ejecutado correctamente")


#Inicializamos variables para guardar los datos del resultado
Z = None                # valor de la función objetivo
rows = None             # número de restricciones
cols = None             # número de variables
status = None           # estado del modelo (OPTIMAL, INFEASIBLE, etc.)
infeasible = False      # indicador de si el modelo es infactible
asignaciones = []       # lista con las asignaciones encontradas
no_asignados = []

#Comprobamos que existe el fichero de la solución
if os.path.exists(fichero_salida_sol):

    #Abrimos el archivo de solución en modo lectura
    with open(fichero_salida_sol, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()  # quitamos espacios a los lados

            #Comprobamos el estado general del modelo (factible o no)
            if line.startswith("Status:"):
                partes = line.split(":")
                if len(partes) > 1:
                    status = partes[1].strip().upper()
                    if "INFEASIBLE" in status or "INTEGER EMPTY" in status:
                        infeasible = True

            #Por si el texto de infactibilidad aparece en otra línea
            elif "INFEASIBLE" in line.upper() or "INTEGER EMPTY" in line.upper():
                infeasible = True

            #Leemos el valor de la función objetivo (Z)
            elif line.startswith("Objective:"):
                partes = line.split("=")
                if len(partes) > 1:
                    try:
                        # Primer número después del signo "="
                        Z = float(partes[1].split()[0])
                    except:
                        Z = None

            #Leemos el número total de restricciones (Rows)
            elif line.startswith("Rows:"):
                partes = line.split()
                if len(partes) > 1:
                    try:
                        rows = int(partes[1])
                    except:
                        rows = None

            #Leemos el número total de variables (Columns)
            elif line.startswith("Columns:"):
                partes = line.split()
                if len(partes) > 1:
                    try:
                        cols = int(partes[1])
                    except:
                        cols = None

            #Buscamos las asignaciones x[a,t,f] que valen 1
            coinc_x = re.match(r".*x\[(\w+),(\w+)\]\s+\*?\s*([0-9]+)", line)
            if coinc_x:
                valor = coinc_x.group(3)
                if valor == "1":
                    a_nombre = coinc_x.group(1)
                    f_nombre = coinc_x.group(2)
                    asignaciones.append((a_nombre, f_nombre))

            #la variable a[i] es 1 si el autobús i-ésimo no está asignado
            coinc_a = re.match(r".*a\[(\w+)\]\s+\*?\s*([0-9]+)", line)
            if coinc_a:
                valor_a = coinc_a.group(2)
                if valor_a == "1":
                    no_asignados.append(coinc_a.group(1))

#Mostramos resutlados por pantalla, este modelo nunca puede ser infactible por cómo esta modelado

print(f"\nZ* = {Z if Z is not None else 'NA'} , variables = {cols if cols is not None else 'NA'} , restricciones = {rows if rows is not None else 'NA'}\n")
print("Asignaciones óptimas:\n")
if len(asignaciones) > 0:
    for a_nombre, f_nombre in asignaciones:
        print(a_nombre, "asignado a", f_nombre)
if len(no_asignados) > 0:
    print("\nAutobuses sin asignar:\n")
    for a_nombre in no_asignados:
        print(a_nombre, "sin asignar")