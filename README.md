# AI cartasur

# Introducción

El presente proyecto determina el scoring interno de clientes a partir de
la información previa que ya se tiene de los clientes.

# Modo de Instalación

El proyecto se maneja absolutamente todo con docker y Makefiles para automatizar algunas tareas.

Con lo cual es condición necesaria tener Docker corriendo y (para los sistemas Unix) make.

## Comandos de Makefile

`make build`: Crea el container

`make shell`: Abre un shell a un container de ai_cartasur

`make up`: arranca ls servicios

`make psql`: abre una consola de base de datos

`make down`: apaga todo y borra los containers

`make db_create`: Crea todas las tablas en la base de datos

`make db_delete`: Borra las tablas de la base de datos **(NO TIENE ROLLBACK o UNDO)**

`make dbshell`: Abre una consola bash en el servidor de base de datos

`drop_database`: Hace drop de todos los datos (**NO TIENE ROLLBACK o UNDO**)

`macos_docker_up`: Levanta el servicio de docker desde una consola (sin UI)


## Cargar datos

Hay que ejecutar cada uno de los scripts de carga uno por uno desde dentro del container:

Clientes y Créditos tarda un poco para crearlos, pero como las cuotas y pagos son archivos MUCHO más grandes, le puse una cierta señal de "vida" para que no nos desesperemos mientras esperamos que corra :-)

``` sh
make shell
cd scripts

python3 load_clientes.py
python3 load_creditos.py
python3 load_cuotas.py
python3 load_pagos.py
```

# Trabajando con SQL

En el proyecto original utilizamos una base de datos NoSQL que funcionó pero no nos dejaba hacer análisis de datos. Ahora estamos usando una base de datos SQL.

Esto nos permitió encontrar algunos problemas en los datos que nos dieron a pensar que los problemas de predicción que estábamos viendo eran problemas relacionados con un desequilibrio en los datos.

## Problemas en los datos (imbalanced-learn)

Uno de los probelmas que encontramos en los datos es que hay datos que parecen estar no balanceados o que tienen algún tipo de problema de muestreo. Por ejemplo hay ciertos ingresos netos que son sospechosamente similares.

Si bien hay valores que es posible que sean iguales, pero hubiéramos esperado que fueran más distribuidos en el dataset (ejemplo hay casi un 2% de los clientes que gana $27677.-)

```
ai_cartasur_db=# select count(*), ROUND((count(*) / 90863.0) * 100, 2) AS rate, ingreso_neto from clientes cl group by ingreso_neto order by count(*) desc limit 20;
 count | rate  | ingreso_neto
-------+-------+--------------
 15682 | 17.26 |            0
  1637 |  1.80 |        27677
  1310 |  1.44 |        21956
  1199 |  1.32 |         8500
  1194 |  1.31 |        39053
   997 |  1.10 |        18047
   944 |  1.04 |        11500
   899 |  0.99 |         6000
   898 |  0.99 |        20443
   883 |  0.97 |        18000
   843 |  0.93 |        46883
   842 |  0.93 |         8600
   814 |  0.90 |        99999
   796 |  0.88 |        38259
   786 |  0.87 |        25000
   785 |  0.86 |        13440
   784 |  0.86 |        27564
   776 |  0.85 |        15000
   768 |  0.85 |        30000
   747 |  0.82 |        56084
```

Para esto vamos a hacer un trabajo de "Random Oversampling and Undersampling for Imbalanced Classification" y ver si esta técnica nos ayuda con las predicciones.
