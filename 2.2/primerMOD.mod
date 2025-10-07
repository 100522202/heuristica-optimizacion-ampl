set TALL;  # Talleres
set AUT;   # Autobuses

param DIST{TALL, AUT} >= 0;   # Distancia del taller t al autobús a

var x{TALL, AUT} binary;      # x[t,a] ∈ {0,1}

minimize DistanciaTotal:
    sum{t in TALL, a in AUT} x[t,a] * DIST[t,a];   # ← termina en ;

s.t. Asignacion{a in AUT}:
    sum{t in TALL} x[t,a] = 1;     # Cada autobús se asigna a un taller

s.t. Permiso{t in TALL}:
    sum{a in AUT} x[t,a] <= 1;     # Cada taller admite como mucho un autobús

end;
