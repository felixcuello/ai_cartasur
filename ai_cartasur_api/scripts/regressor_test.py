#!/usr/bin/env python3

import os
import sys
import numpy
import psycopg2
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from random_forest import random_forest

conn = psycopg2.connect("host={} dbname={} user={} password={}".
                        format(
                            os.environ['POSTGRES_HOST'],
                            os.environ['POSTGRES_DB'],
                            os.environ['POSTGRES_USER'],
                            os.environ['POSTGRES_PASSWORD']
                        ))

sql = """
SELECT
  ------------------------------------
  -- clientes
  ------------------------------------
  COALESCE(cl.sexo, 'D') AS sexo,
  COALESCE(CAST(ROUND(date_part('year', AGE(cl.fnac))::numeric, -1) AS integer), 0) AS edad,
  COALESCE(CAST(ROUND(cl.ingreso_neto::numeric, -4) AS integer), 0) AS ingreso_neto,
  cl.provincia_per,
  cl.tipolaboral,
  cl.metal,
  COALESCE(CAST(cl.operaciones AS integer), 0) AS operaciones,
  COALESCE(CAST(ROUND(cl.refines::numeric, -1) AS integer), 0) AS refines,
  COALESCE(CAST(ROUND(cl.peor_atraso_hist::numeric, -1) AS integer), 0) AS peor_atraso_hist,
  ------------------------------------
  -- creditos
  ------------------------------------
  COALESCE(CAST(ROUND(cr.monto::numeric, -4) AS integer), 0) AS monto,
  recibo,
  COALESCE(CAST(ROUND(cr.siisa_montomorasbcra::numeric, -5) AS integer), 0) AS siisa_montomorasbcra,
  COALESCE(siisa_cantmorasbcra, 0) AS siisa_cantmorasbcra,
  COALESCE(siisa_reldepmeses, 0) AS siisa_reldepmeses,
  COALESCE(CAST(ROUND(cr.veraz_score::numeric, -2) AS integer), 0) AS veraz_score,
  COALESCE(siisa_sesmodelo, 0) AS siisa_sesmodelo,
  COALESCE(siisa_consultasano, 0) AS siisa_consultasano,
--  siisa_sectorlaboral,  -- Lo excluyo porque no sé si sirve para algo
-- siisa_ingreso,         -- Lo excluyo porque los datos se ven raros
-- siisa_compromiso       -- Lo excluyo porque los datos se ven raros
-- siisa_maxbcra24m
-- siisa_score
-- siisa_scorepoblacion
-- siisa_maxbcra12mi
-- siisa_cantmoras
-- siisa_maxbcra6m
-- siisa_consultasseismeses
-- siisa_sescat
-- siisa_consultasdosano
-- siisa_consultastresmeses
-- siisa_consultasmes
  ROUND(score::numeric, -1) AS score -- SCORE está agrupado cada 10
FROM clientes cl
  INNER JOIN creditos cr ON cl.id_cliente = cr.id_cliente
"""

# -------------------------------------------------------------
#  Convierte SQL en un dataframe de Pandas
# -------------------------------------------------------------
datos = pd.read_sql_query(sql, conn)


# -------------------------------------------------------------
#  Normalizacion
# -------------------------------------------------------------
datos.dropna()
columnas_categorizables = [
    'sexo', 'provincia_per', 'tipolaboral', 'metal', # clientes
    'recibo', 'siisa_reldepmeses', 'veraz_score', 'siisa_sesmodelo' # creditos
]

for columna in columnas_categorizables:
    datos[columna] = datos[columna].astype('category').cat.codes

# -------------------------------------------------------------
#  Probamos un regresor
# -------------------------------------------------------------
regresor = random_forest(datos)
