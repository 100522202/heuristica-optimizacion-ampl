set FRAN;
set AUT;

#Parametros
param DIST{AUT, FRAN} >= 0;   #distancia del bus i a la franja s (o al taller si la franja no cambia la distancia)
param EUR{AUT} >=0;           #Nuestro Kd (euros por KM del bus asignado)
param PEN{AUT} >= 0;          #Nuestro Kp (penalización en euros por pasajero (bus no asignado)) 
param PAS{AUT} >= 0;          #Cantidad de pasajeros en el Bus i

#Variables de decisión
var x{AUT, FRAN} binary;      #x[i,s] = 1 si el bus i está asignado a la franja s
var a{AUT} binary;            #a[i] = 1 si el bus i NO está asignado a ninguna franja


# Función objetivo 
minimize Perdidas:
    sum{i in AUT, s in FRAN}  (EUR[i] * DIST[i, s] * x[i,s])   #Coste por asignar el bus i a la franja s
  + sum{i in AUT} PEN[i] * PAS[i] * a[i];                      #Penalización por no asignar el bus i


# Restricción 1: Un autobús puede estar asignado o no estarlo (pero no ambas cosas)
s.t. Asignado{i in AUT}:
    sum{s in FRAN} x[i,s] + a[i] = 1; 


# Restricción 2: Cada franja admite máximo un autobús
s.t. MaximFranja{s in FRAN}:
    sum{i in AUT} x[i,s] <= 1; 


solve;

#Salida de resultados
printf "=== SOLUCION ===\n";
printf "Perdidas totales = %g\n", Perdidas;

for {i in AUT: a[i] > 0.5}
    printf "Bus %s NO asignado (penalizacion = %g)\n", i, PEN[i]*PAS[i];

for {i in AUT, s in FRAN: x[i,s] > 0.5}
    printf "Bus %s -> Franja %s (coste = %g)\n", i, s, EUR[i]*DIST[i,s];

end;