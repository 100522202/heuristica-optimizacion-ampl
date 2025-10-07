import json, os

with open("2.2\datos.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

autobuses = datos["AUTOBUSES"]   #Obtiene los datos del json de autbous y devulve la lista correspondiente ["a1","a2","a3","a4","a5"]
talleres  = datos["TALLERES"]    # Obtiene los datos del json de talleres y devulve la lista correspondiente["t1","t2","t3","t4","t5"]
dist      = datos["DISTANCIA"]   # Obtiene los datos de diastancia del json dist["t1"]["a1"] = número

#Creamos el texto que se encontrara dentro de nuestro .dat
texto = ""
texto += "data;\n\n"  # <<--- añadido al principio del fichero
texto += "set TALL := " + " ".join(talleres) + ";\n\n"  # Añadimos a set TALL la lista de talleres obtenida anteriormente del json
texto += "set AUT := " + " ".join(autobuses) + ";\n\n"  # Añadimos a set AUT la lista de autobuses obtenida anteriormente del json

#Aqui realizamos un bucle para rellenar la matriz que representa todas las
# diastancias pero primero añadimos la lista de autbous para representar las
# columnas de la matriz y luego añadiremos las filas con los talleres
texto += "param DIST : " + " ".join(autobuses) + " :=\n"
for t in talleres:
    linea = t + " "
    for a in autobuses:
        linea += str(dist[t][a]) + " "
    texto += "  " + linea + "\n"
#Indicamos el final con un ;
texto += ";\n\nend;\n"  # <<--- añadido al final del fichero

#Abrimos un archivo instancia.dat al que escribiremos donde
# escribiremos el texto generado en la variable anterior
with open("instancia.dat", "w", encoding="utf-8") as f:
    f.write(texto)

print("Generado instancia.dat")

#Resuelve el glpk con os.system que es similar a escribir en la terminal el
# contenido descrito en la variable "comando"
comando = "glpsol --model 2.2\primerMOD.mod --data instancia.dat -o solucion.txt"
os.system(comando)

print("GLPK ejecutado correctamente")
