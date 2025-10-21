set FRAN;
set AUT;

#Parametros escalares
param kd >= 0;                  # euros por km si se asigna el bus
param kp >= 0;                  # euros por pasajero si NO se asigna el bus

#Parametros unidimensionales
param DIST{AUT} >= 0;           # distancia del bus i al taller
param PAS{AUT}  >= 0;           # pasajeros del bus i

#Variables de decisión
var x{AUT, FRAN} binary;        # x[i,s] = 1 si el bus i está asignado a la franja s
var a{AUT}       binary;        # a[i] = 1 si el bus i NO está asignado a ninguna franja

# Función objetivo 
minimize Perdidas:
    sum{i in AUT, s in FRAN} (kd * DIST[i] * x[i,s])    # Coste por asignar el bus i a la franja s
  + sum{i in AUT} (kp * PAS[i] * a[i]);                 # Penalización por no asignar el bus i

# Restricción 1: Un autobús puede estar asignado o no estarlo (exactamente una opción)
s.t. Asignado{i in AUT}:
    sum{s in FRAN} x[i,s] + a[i] = 1;

# Restricción 2: Cada franja admite máximo un autobús
s.t. MaximFranja{s in FRAN}:
    sum{i in AUT} x[i,s] <= 1;

end;
