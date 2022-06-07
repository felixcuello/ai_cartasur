# AI cartasur

## Introducción

El presente proyecto determina el scoring interno de clientes a partir de
la información previa que ya se tiene de los clientes.

## Modo de Instalación

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
