# Modelado Matemático y Optimización Lineal - Heurística y Optimización

Práctica 1 de la asignatura **Heurística y Optimización (UC3M)**.

---

## 📌 Descripción

Formulación y resolución de problemas de **Programación Lineal (PL)** y **Programación Entera Mixta (MIP)** utilizando el lenguaje de modelado algebraico **AMPL** y solvers de optimización (**GLPK / CPLEX**).

El proyecto incluye:
* Modelado matemático formal (variables de decisión, función objetivo y restricciones).
* Archivos de modelo (`.mod`) y archivos de datos (`.dat`) para distintas instancias de prueba.
* Scripts auxiliares de generación y análisis de resultados en Python y hojas de cálculo (`.ods`).

---

## 🛠️ Uso con AMPL

```bash
ampl
ampl: model parte1.mod;
ampl: data parte1.dat;
ampl: option solver cplex; # o glpk
ampl: solve;
ampl: display _nvars, _ncons, _objval;
```
