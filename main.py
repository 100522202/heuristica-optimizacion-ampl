import json  # Para leer el fichero JSON
from pathlib import Path  # Para escribir el .dat

#Pedimos el nombre del fichero JSON al usuario
ruta_json = input("Introduce el nombre del fichero JSON")

#Leemos el JSON
with open(ruta_json, "r", encoding="utf-8") as f:
   datos = json.load(f)

#Extraemos los datos y la matriz  del json
autobuses = datos["AUTOBUSES"]   # Lista: ["a1","a2",...]
talleres = datos["TALLERES"]     # Lista: ["t1","t2",...]
distancia = datos["DISTANCIA"]   # Diccionario: distancia["t1"]["a1"] = número

#Nos aseguramos de que para cada taller haya autobuses
# Si falta alguna distancia, lanzamos un mensaje de error.
for t in talleres:
   if t not in distancia:
       raise ValueError("Falta la fila del taller '" + t + "' dentro de 'DISTANCIA' en el JSON.")
   for a in autobuses:
       if a not in distancia[t]:
           raise ValueError("Falta la distancia para taller '" + t + "' y autobús '" + a + "' en 'DISTANCIA'.")

# Empezamos a crear el contenido del .dat en texto
texto = ""
#Conjunto de talleres
texto += "TALL := " + " ".join(talleres) + ";\n\n"
#Conjunto de autobuses
texto += "AUT:= " + " ".join(autobuses) + ";\n\n"
# Matriz de distancias: filas=talleres, columnas=autobuses
texto += "DIST : " + " ".join(autobuses) + " :=\n"

for t in talleres:
   # Escribimos el nombre del taller
   fila = t + " "
   for a in autobuses:
       #Añadimos las distancias del taller a cada autbous
       fila += str(distancia[t][a]) + " "
   # Guardamos la linea al final del texto
   texto += "  " + fila + "\n"
#Se añade al final un punto y coma marcando que se han añadido todas las filas
texto += ";\n"

#Escribimos el archivo de salida .dat
ruta_salida = Path("instancia.dat")
with open(ruta_salida, "w", encoding="utf-8") as f:
   f.write(texto)

print("Fichero .dat generado correctamente:")
print(ruta_salida.resolve())
import json  # Para leer el fichero JSON
from pathlib import Path  # Para escribir el .dat

#Pedimos el nombre del fichero JSON al usuario
ruta_json = input("Introduce el nombre del fichero JSON")

#Leemos el JSON
with open(ruta_json, "r", encoding="utf-8") as f:
   datos = json.load(f)

#Extraemos los datos y la matriz  del json
autobuses = datos["AUTOBUSES"]   # Lista: ["a1","a2",...]
talleres = datos["TALLERES"]     # Lista: ["t1","t2",...]
distancia = datos["DISTANCIA"]   # Diccionario: distancia["t1"]["a1"] = número

#Nos aseguramos de que para cada taller haya autobuses
# Si falta alguna distancia, lanzamos un mensaje de error.
for t in talleres:
   if t not in distancia:
       raise ValueError("Falta la fila del taller '" + t + "' dentro de 'DISTANCIA' en el JSON.")
   for a in autobuses:
       if a not in distancia[t]:
           raise ValueError("Falta la distancia para taller '" + t + "' y autobús '" + a + "' en 'DISTANCIA'.")

# Empezamos a crear el contenido del .dat en texto
texto = ""
#Conjunto de talleres
texto += "TALL := " + " ".join(talleres) + ";\n\n"
#Conjunto de autobuses
texto += "AUT:= " + " ".join(autobuses) + ";\n\n"
# Matriz de distancias: filas=talleres, columnas=autobuses
texto += "DIST : " + " ".join(autobuses) + " :=\n"

for t in talleres:
   # Escribimos el nombre del taller
   fila = t + " "
   for a in autobuses:
       #Añadimos las distancias del taller a cada autbous
       fila += str(distancia[t][a]) + " "
   # Guardamos la linea al final del texto
   texto += "  " + fila + "\n"
#Se añade al final un punto y coma marcando que se han añadido todas las filas
texto += ";\n"

#Escribimos el archivo de salida .dat
ruta_salida = Path("instancia.dat")
with open(ruta_salida, "w", encoding="utf-8") as f:
   f.write(texto)

print("Fichero .dat generado correctamente:")
print(ruta_salida.resolve())
