#!env python
import os, sys, re, subprocess

# Comprobamos argumentos
if len(sys.argv) != 3:
    print("Uso: ./gen-1.py <fichero-entrada> <fichero-datos>")
    sys.exit(1)

fichero_entrada = sys.argv[1]       # fichero de entrada (.in)
fichero_salida_dat = sys.argv[2]    # fichero .dat
fichero_salida_sol = "solucion221.txt"          # salida de GLPK con --output

# Leemos el fichero de entrada
with open(fichero_entrada, "r", encoding="utf-8") as f:
    lineas = [l.strip() for l in f if l.strip() != ""]

n, m = map(int, lineas[0].split())
kd, kp = map(float, lineas[1].split())
d = list(map(float, lineas[2].split()))
p = list(map(float, lineas[3].split()))

# Creamos listas de nombres
autobuses = [f"a{i+1}" for i in range(m)]
franjas = [f"s{j+1}" for j in range(n)]

# Generamos el contenido del fichero .dat
texto  = "data;\n\n"
texto += "set AUT := " + " ".join(autobuses) + ";\n\n"
texto += "set FRAN := " + " ".join(franjas) + ";\n\n"
texto += f"param kd := {kd};\nparam kp := {kp};\n\n"

texto += "param DIST :=\n"
for i in range(m):
    texto += f"{autobuses[i]} {d[i]}\n"
texto += ";\n\n"

texto += "param PAS :=\n"
for i in range(m):
    texto += f"{autobuses[i]} {p[i]}\n"
texto += ";\n\nend;\n"

# Guardamos el .dat
with open(fichero_salida_dat, "w", encoding="utf-8") as f:
    f.write(texto)

print("Generado " + fichero_salida_dat + " correctamente")

# Ejecutamos GLPK y redirigimos su salida a un fichero

resultado_glpk = subprocess.run(
    ["glpsol", "--model", "parte-2-1.mod", "--data", fichero_salida_dat, "--output", fichero_salida_sol],
    capture_output=True, text=True
)

# Analizamos la salida estándar para ver si el modelo es infactible
es_infactible = bool(re.search(r"INFEASIBLE|INTEGER\s+EMPTY", resultado_glpk.stdout, re.IGNORECASE))

# Inicializamos variables
valor_objetivo = None
num_restricciones = None
num_variables = None
autobuses_asignados = set()
autobuses_no_asignados = set()

# Detectar infactibilidad desde stdout
if re.search(r"INFEASIBLE|INTEGER\s+EMPTY", resultado_glpk.stdout, re.IGNORECASE):
    es_infactible = True

# Analizamos el fichero de salida generado por GLPK
if os.path.exists(fichero_salida_sol):
    with open(fichero_salida_sol, "r", encoding="utf-8", errors="ignore") as archivo_salida:
        contenido_salida = archivo_salida.read()

    # Capturamos valores principales
    match_objetivo = re.search(r"Objective:\s+.+?=\s*([-+]?\d+(?:\.\d+)?)", contenido_salida)
    match_filas = re.search(r"Rows:\s+(\d+)", contenido_salida)
    match_columnas = re.search(r"Columns:\s+(\d+)", contenido_salida)

    if match_objetivo:
        valor_objetivo = float(match_objetivo.group(1))
    if match_filas:
        num_restricciones = int(match_filas.group(1))
    if match_columnas:
        num_variables = int(match_columnas.group(1))

    # Autobuses asignados: líneas tipo  x[a3,s1]  *  1 ...
    for match in re.finditer(r"x\[\s*(\w+)\s*,\s*(\w+)\s*\]\s+\*?\s*([0-9]+)", contenido_salida):
        autobus, franja, valor = match.groups()
        if autobus.startswith("a") and valor == "1":
            autobuses_asignados.add(autobus)

    # Autobuses no asignados: líneas tipo  a[a4]  *  1 ...
    for match in re.finditer(r"a\[\s*(\w+)\s*\]\s+\*?\s*([0-9]+)", contenido_salida):
        autobus, valor = match.groups()
        if autobus.startswith("a") and valor == "1":
            autobuses_no_asignados.add(autobus)

# Mostramos resultados por pantalla
if es_infactible:
    print("El modelo es infactible, no existen asignaciones válidas.\n")
else:
    print(f"Z* = {valor_objetivo if valor_objetivo is not None else 'NA'} , "
          f"variables = {num_variables if num_variables is not None else 'NA'} , "
          f"restricciones = {num_restricciones if num_restricciones is not None else 'NA'}\n")

    print("Autobuses asignados:\n")
    if autobuses_asignados:
        for autobus in sorted(autobuses_asignados):
            print(autobus)
    else:
        print("(No se encontraron autobuses asignados)")

    # Autobuses sin asignar = explícitos + los que no aparecen en asignados
    autobuses_sin_asignar = sorted(autobuses_no_asignados | (set(autobuses) - autobuses_asignados))
    if autobuses_sin_asignar:
        print("\nAutobuses sin asignar:\n")
        for autobus in autobuses_sin_asignar:
            print(autobus)

# Eliminamos el fichero temporal de salida
os.remove(fichero_salida_sol)