set TALL;   # Talleres
set AUT;    # Autobuses
set FRAN;   # Franjas

param CIJ{AUT,AUT} >= 0;                 # Pasajeros en común entre autobuses i y j
# Nota: en parámetros no existe el dominio 'binary'. Si quieres restringir a 0/1:
# param OIJ{FRAN,TALL} >= 0, <= 1, integer;
param OIJ{FRAN,TALL};                    # 1 si la franja f está disponible en el taller t

# Variable: 1 si el bus i va al taller t en la franja f
# Solo se crean para combinaciones válidas (OIJ=1)
# Esto reduce el número de variables activas (y restricciones) y evita combinaciones imposibles
var x{i in AUT, t in TALL, f in FRAN: OIJ[f,t]=1} binary;

# Variable: 1 si los autobuses i y j coinciden en la misma franja f
# Solo se crean para pares (i,j) con pasajeros comunes (CIJ[i,j]>0)
# Así eliminamos variables y restricciones que no afectan a la función objetivo ni al resultado óptimo
# Esta reducción disminuye el tamaño del modelo (menos variables y restricciones) sin alterar las soluciones factibles
var y{i in AUT, j in AUT, f in FRAN: i < j and CIJ[i,j] > 0} binary;

# FUNCIÓN OBJETIVO
# Minimiza el impacto total de coincidencias de pasajeros en una misma franja
# Se consideran únicamente las parejas de autobuses con CIJ>0 (es decir, que comparten pasajeros)
minimize Impacto:
    sum{i in AUT, j in AUT, f in FRAN: i < j and CIJ[i,j] > 0} CIJ[i,j] * y[i,j,f];

# RESTRICCIONES

# 1. Cada autobús se asigna a un único taller y franja
# Se suman únicamente las combinaciones válidas según OIJ[f,t]
s.t. AsignacionUnica{i in AUT}:
    sum{t in TALL, f in FRAN: OIJ[f,t]=1} x[i,t,f] = 1;

# 2. Cada par (taller, franja) puede tener como máximo un autobús
# Si OIJ[f,t]=0, esa combinación directamente no genera restricción
s.t. CapacidadFranjaTaller{t in TALL, f in FRAN: OIJ[f,t]=1}:
    sum{i in AUT} x[i,t,f] <= 1;

# 3. Definir coincidencia en franja (y)
# Suficiente con la cota inferior dado que CIJ>=0 y minimizamos
# Si ambos autobuses están asignados a la misma franja (en cualquier taller),
# entonces y[i,j,f] debe valer 1
# Solo se definen para pares de autobuses con CIJ>0, ya que los demás no afectan al impacto
s.t. Y_coincidencia{i in AUT, j in AUT, f in FRAN: i < j and CIJ[i,j] > 0}:
    y[i,j,f] >= sum{t in TALL: OIJ[f,t]=1} x[i,t,f]
              + sum{t in TALL: OIJ[f,t]=1} x[j,t,f] - 1;

end;
