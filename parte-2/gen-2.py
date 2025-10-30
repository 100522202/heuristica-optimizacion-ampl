#!/usr/bin/env python3
import os
import sys
import re
import subprocess


def leer_entrada(fichero_entrada):
    """Lee el fichero de entrada y devuelve sus líneas sin espacios vacíos."""
    with open(fichero_entrada, "r", encoding="utf-8") as f:
        lineas = [linea.strip() for linea in f if linea.strip()]
    return lineas


def procesar_datos(lineas):
    """Procesa las líneas del fichero de entrada y devuelve las matrices y parámetros."""
    f, a, t = map(int, lineas[0].split())

    cij = [list(map(int, lineas[i].split())) for i in range(1, a + 1)]
    oij = [list(map(int, lineas[i].split())) for i in range(a + 1, a + f + 1)]

    autobuses = [f"a{i+1}" for i in range(a)]
    franjas = [f"s{j+1}" for j in range(f)]
    talleres = [f"t{k+1}" for k in range(t)]

    return f, a, t, cij, oij, autobuses, franjas, talleres


def generar_dat(fichero_salida, autobuses, talleres, franjas, cij, oij):
    """Genera el contenido del fichero .dat y lo guarda."""
    texto = "data;\n\n"
    texto += f"set AUT := {' '.join(autobuses)};\n\n"
    texto += f"set TALL := {' '.join(talleres)};\n\n"
    texto += f"set FRAN := {' '.join(franjas)};\n\n"

    texto += "param CIJ : " + " ".join(autobuses) + " :=\n"
    for i, a in enumerate(autobuses):
        texto += " " + a + " " + " ".join(map(str, cij[i])) + "\n"
    texto += ";\n\n"

    texto += "param OIJ : " + " ".join(talleres) + " :=\n"
    for i, s in enumerate(franjas):
        texto += " " + s + " " + " ".join(map(str, oij[i])) + "\n"
    texto += ";\n\nend;\n"

    with open(fichero_salida, "w", encoding="utf-8") as f:
        f.write(texto)


def ejecutar_glpk(fichero_dat, fichero_sol):
    """Ejecuta GLPK y devuelve la salida completa y si es infactible."""
    resultado = subprocess.run(
        ["glpsol", "--model", "parte-2-2.mod", "--data", fichero_dat, "--output", fichero_sol],
        capture_output=True, text=True
    )

    salida = resultado.stdout
    infactible = bool(re.search(
        r"(HAS\s+NO\s+PRIMAL\s+FEASIBLE\s+SOLUTION|NO\s+PRIMAL\s+FEASIBLE\s+SOLUTION\s+FOUND|INFEASIBLE|INTEGER\s+EMPTY)",
        salida, re.IGNORECASE
    ))

    if os.path.exists(fichero_sol):
        with open(fichero_sol, "r", encoding="utf-8", errors="ignore") as f:
            salida += "\n" + f.read()

    return salida, infactible


def extraer_resultados(salida):
    """Extrae valores del resultado de GLPK."""
    obj = re.search(r"Objective:\s+.+?=\s*([-+]?\d+(?:\.\d+)?)", salida)
    rows = re.search(r"Rows:\s+(\d+)", salida)
    cols = re.search(r"Columns:\s+(\d+)", salida)

    valor_obj = float(obj.group(1)) if obj else None
    restricciones = int(rows.group(1)) if rows else None
    variables = int(cols.group(1)) if cols else None

    asignaciones = set()
    for m in re.finditer(r"x\[\s*(a\d+)\s*,\s*(t\d+)\s*,\s*(s\d+)\s*\]\s+\*?\s*([01])", salida):
        a, t, s, v = m.groups()
        if v == "1":
            asignaciones.add((a, t, s))

    return valor_obj, restricciones, variables, asignaciones


def mostrar_resultados(valor_obj, restricciones, variables, asignaciones, infactible):
    """Muestra en pantalla los resultados finales."""
    if infactible:
        print("\nEl modelo es infactible: no existen asignaciones válidas.\n")
        return

    print(f"\nZ* = {valor_obj if valor_obj is not None else 'NA'} , "
          f"variables = {variables if variables is not None else 'NA'} , "
          f"restricciones = {restricciones if restricciones is not None else 'NA'}\n")

    if asignaciones:
        print("Asignaciones óptimas:\n")
        for a, t, s in sorted(asignaciones, key=lambda x: int(x[0][1:])):
            print(f"{a} asignado a {t}, {s}")
    else:
        print("El modelo es infactible: no existen asignaciones válidas.")


def main():
    if len(sys.argv) != 3:
        print("Uso: ./gen-2.py <fichero-entrada> <fichero-datos>")
        sys.exit(1)

    fichero_entrada, fichero_salida_dat = sys.argv[1], sys.argv[2]
    fichero_salida_sol = "solucion222.txt"

    lineas = leer_entrada(fichero_entrada)
    f, a, t, cij, oij, autobuses, franjas, talleres = procesar_datos(lineas)
    generar_dat(fichero_salida_dat, autobuses, talleres, franjas, cij, oij)

    salida, infactible = ejecutar_glpk(fichero_salida_dat, fichero_salida_sol)
    valor_obj, restricciones, variables, asignaciones = extraer_resultados(salida)

    mostrar_resultados(valor_obj, restricciones, variables, asignaciones, infactible)

    if os.path.exists(fichero_salida_sol):
        os.remove(fichero_salida_sol)


if __name__ == "__main__":
    main()
