#!env python3
import os, sys, re, subprocess

#Comprobamos argumentos
if len(sys.argv) != 3:
    print("Uso: ./gen-2.py <fichero-entrada> <fichero-datos>")
    sys.exit(1)

fichero_entrada = sys.argv[1]   # fichero de entrada
fichero_salida_dat = sys.argv[2]  # fichero .dat
fichero_salida_sol = "solucion222.txt"

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
# Ejecutamos GLPK sin redirigir salidas a ficheros intermedios
resultado_glpk = subprocess.run(
    ["glpsol", "--model", "parte-2-2.mod", "--data", fichero_salida_dat, "--output", fichero_salida_sol],
    capture_output=True, text=True
)

salida_total = resultado_glpk.stdout
es_infactible = False
# Analizar posible infactibilidad también desde stdout
if re.search(r"(HAS\s+NO\s+PRIMAL\s+FEASIBLE\s+SOLUTION|NO\s+PRIMAL\s+FEASIBLE\s+SOLUTION\s+FOUND|INFEASIBLE|INTEGER\s+EMPTY)", salida_total, re.IGNORECASE):
    es_infactible = True
else:
    es_infactible = False

# Intentar leer fichero de salida completo si existe
if os.path.exists(fichero_salida_sol):
    with open(fichero_salida_sol, "r", encoding="utf-8", errors="ignore") as f:
        salida_total += "\n" + f.read()

# Capturamos valores numéricos principales
match_obj = re.search(r"Objective:\s+.+?=\s*([-+]?\d+(?:\.\d+)?)", salida_total)
match_rows = re.search(r"Rows:\s+(\d+)", salida_total)
match_cols = re.search(r"Columns:\s+(\d+)", salida_total)

if match_obj:
    valor_objetivo = float(match_obj.group(1))
if match_rows:
    num_restricciones = int(match_rows.group(1))
if match_cols:
    num_variables = int(match_cols.group(1))

# Capturamos asignaciones x[a,t,f] = 1
asignaciones = set()
for match in re.finditer(r"x\[\s*(a\d+)\s*,\s*(t\d+)\s*,\s*(s\d+)\s*\]\s+\*?\s*([01])", salida_total):
    autobus, taller, franja, valor = match.groups()
    if valor == "1":
        asignaciones.add((autobus, taller, franja))


# MOSTRAMOS RESULTADOS POR PANTALLA
if es_infactible:
    print("\nEl modelo es infactible: no existen asignaciones válidas.\n")
else:
    print(f"\nZ* = {valor_objetivo if valor_objetivo is not None else 'NA'} , "
          f"variables = {num_variables if num_variables is not None else 'NA'} , "
          f"restricciones = {num_restricciones if num_restricciones is not None else 'NA'}\n")

    if asignaciones:
        print("Asignaciones óptimas:\n")
        for autobus, taller, franja in sorted(asignaciones, key=lambda x: int(x[0][1:])):
            print(f"{autobus} asignado a {taller}, {franja}")
    else:
        print("El modelo es infactible: no existen asignaciones válidas.)")


if os.path.exists(fichero_salida_sol):
    os.remove(fichero_salida_sol)