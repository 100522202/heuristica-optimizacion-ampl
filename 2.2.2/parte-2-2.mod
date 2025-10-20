set TALL;   # Talleres
set AUT;    # Autobuses
set FRAN;   # Franjas

param CIJ{AUT,AUT} >=0;             # Pasajeros que usan los autbouses i y j
param OIJ{FRAN, TALL} binary;          # asignar el bus i a (franja k, taller j)

var x{AUT, TALL, FRAN} binary;         # 1 si el bus i se asigna a la franja f del taller t
var y{AUT, AUT, FRAN} binary; #variable binaria que indica si dos autbouses coinciden o no

# Objetivo: minimizar el numero de usuarios asignados a la misma franja en talleres distintos
minimize DistanciaTotal:
    sum{i in AUT, j in AUT, f in FRAN} CIJ[i,j] * y[i,j,f];

# Cada autobús debe ser asigando a un único taller y una única franja
s.t. AsignacionUnica{i in AUT}:
    sum{t in TALL,f in FRAN} x[i,t,f]=1;

# Cada par franja taller soo admite como maximo un autobus
s.t. AsignacionUnica{t in TALL,f in FRAN}:
    sum{i in AUT} x[i,t,f]<=1;

#El aubous solo puede asiganrse a combinaciones franja taller dispoibes
s.t. AsignacionUnica{i i AUT,t in TALL,f in FRAN}:
    x[i,t,f]<=OIJ[f,t];

#Restriccion para establecer "y" en 1 cuando dos autbouses coinciden

# Restricción 1: si el autobús i NO está asignado a la franja f, entonces y[i,j,f] debe ser 0
s.t. restriccion1{i in AUT, j in AUT, f in FRAN: i != j}:
    y[i,j,f] <= sum{t in TALL} x[i,t,f];

# Restricción 2: si el autobús j NO está asignado a la franja f, entonces y[i,j,f] debe ser 0
s.t. restriccion2{i in AUT, j in AUT, f in FRAN: i != j}:
    y[i,j,f] <= sum{t in TALL} x[j,t,f];

# Restricción 3: si AMBOS autobuses están asignados a la franja f (en cualquier taller),
# entonces y[i,j,f] se fuerza a 1
s.t. restriccion3{i in AUT, j in AUT, f in FRAN: i != j}:
    y[i,j,f] >= sum{t in TALL} x[i,t,f] + sum{t in TALL} x[j,t,f] - 1;
