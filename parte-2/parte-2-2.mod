set TALL;   # Talleres
set AUT;    # Autobuses
set FRAN;   # Franjas

param CIJ{AUT,AUT} >=0;             # Pasajeros que usan los autbouses i y j
param OIJ{FRAN, TALL} binary;       # indica si la combinación (franja, taller) está disponible

var x{AUT, TALL, FRAN} binary;      # 1 si el bus i se asigna a la franja f del taller t

# Variable binaria que indica si dos autobuses coinciden en la misma franja
# Se definen para i < j para evitar duplicados (y[i,j,f] = y[j,i,f])
var y{ i in AUT, j in AUT, f in FRAN : i < j } binary;

# Objetivo: minimizar el número de usuarios asignados a la misma franja en talleres distintos
minimize Impacto:
    sum{ i in AUT, j in AUT, f in FRAN : i < j } CIJ[i,j] * y[i,j,f];

# Cada autobús debe ser asignado a un único taller y una única franja
s.t. AsignacionUnica1{i in AUT}:
    sum{t in TALL, f in FRAN} x[i,t,f] = 1;

# Cada par (taller, franja) solo admite como máximo un autobús
s.t. AsignacionUnica2{t in TALL, f in FRAN}:
    sum{i in AUT} x[i,t,f] <= 1;

# El autobús solo puede asignarse a combinaciones (franja, taller) disponibles
s.t. AsignacionUnica3{i in AUT, t in TALL, f in FRAN}:
    x[i,t,f] <= OIJ[f,t];

# Restricciones para establecer "y" en 1 cuando dos autobuses coinciden

# Restricción 1: si el autobús i NO está asignado a la franja f, entonces y[i,j,f] debe ser 0
s.t. restriccion1{i in AUT, j in AUT, f in FRAN : i < j}:
    y[i,j,f] <= sum{t in TALL} x[i,t,f];

# Restricción 2: si el autobús j NO está asignado a la franja f, entonces y[i,j,f] debe ser 0
s.t. restriccion2{i in AUT, j in AUT, f in FRAN : i < j}:
    y[i,j,f] <= sum{t in TALL} x[j,t,f];

# Restricción 3: si ambos autobuses están asignados a la franja f (en cualquier taller),
# entonces y[i,j,f] se fuerza a 1
s.t. restriccion3{i in AUT, j in AUT, f in FRAN : i < j}:
    y[i,j,f] >= sum{t in TALL} x[i,t,f] + sum{t in TALL} x[j,t,f] - 1;

end;
