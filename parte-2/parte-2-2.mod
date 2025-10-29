set TALL;   # Talleres
set AUT;    # Autobuses
set FRAN;   # Franjas

param CIJ{AUT,AUT} >= 0;      # Pasajeros en común entre autobuses i y j
param OIJ{FRAN,TALL} binary;  # 1 si la franja f está disponible en el taller t

# Variable: 1 si el bus i va al taller t en la franja f
# Solo se crean para combinaciones válidas (OIJ=1)
var x{i in AUT, t in TALL, f in FRAN: OIJ[f,t]=1} binary;

# Variable: 1 si los autobuses i y j coinciden en la misma franja f
var y{i in AUT, j in AUT, f in FRAN: i < j} binary;

# ----- FUNCIÓN OBJETIVO -----
minimize Impacto:
    sum{i in AUT, j in AUT, f in FRAN: i < j} CIJ[i,j] * y[i,j,f];

# ----- RESTRICCIONES -----

# 1. Cada autobús se asigna a un único taller y franja
s.t. UnicoPorBus{i in AUT}:
    sum{t in TALL, f in FRAN: OIJ[f,t]=1} x[i,t,f] = 1;

# 2. Cada taller y franja puede tener como máximo un autobús
s.t. CapacidadTaller{t in TALL, f in FRAN: OIJ[f,t]=1}:
    sum{i in AUT} x[i,t,f] <= 1;

# 3. Definir coincidencia en franja (y)
s.t. Y1{i in AUT, j in AUT, f in FRAN: i < j}:
    y[i,j,f] <= sum{t in TALL: OIJ[f,t]=1} x[i,t,f];

s.t. Y2{i in AUT, j in AUT, f in FRAN: i < j}:
    y[i,j,f] <= sum{t in TALL: OIJ[f,t]=1} x[j,t,f];

s.t. Y3{i in AUT, j in AUT, f in FRAN: i < j}:
    y[i,j,f] >= sum{t in TALL: OIJ[f,t]=1} x[i,t,f]
              + sum{t in TALL: OIJ[f,t]=1} x[j,t,f] - 1;

end;
