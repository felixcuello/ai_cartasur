#!/usr/local/bin/python3

# ==========================================================================
#   Carga los creditos en el postgres
# ==========================================================================
import os
import csv
import pandas as pd
import psycopg2

conn = psycopg2.connect("host={} dbname={} user={} password={}".
                        format(
                            os.environ['POSTGRES_HOST'],
                            os.environ['POSTGRES_DB'],
                            os.environ['POSTGRES_USER'],
                            os.environ['POSTGRES_PASSWORD']
                        ))

creditos = open('/data/creditos_up.csv', encoding='iso-8859-1')
csvreader = csv.reader(creditos, delimiter='|')
next(csvreader) # saltear el header

cursor = conn.cursor()
cursor.execute("DELETE FROM creditos;")

def string_to_float(string):
    if string == '':
        return 'NULL'
    else:
        return float(string.replace(",", "."))

def string_to_int(string):
    if string == '' or string == 'H' or string == 'T':
        return 'NULL'
    else:
        return int(string_to_float(string))

def string_or_null(string):
    if(string == '' or string == None or string == 'NULL'):
        return "NULL"
    else:
        return "'%s'" % (string)

#  0  id_credito INTEGER PRIMARY KEY,
#  1  tdoc VARCHAR,
#  2  ndoc VARCHAR,
#  3  fechainforme date,
#  4  fliquidacion TIMESTAMP WITHOUT TIME ZONE,
#  5  codigo INTEGER,
#  6  monto FLOAT,
#  7  sucursal VARCHAR,
#  8  nombre VARCHAR,
#  9  recibo VARCHAR,
# 10  clase_plan VARCHAR,
# 11  pkey_job VARCHAR,
# 12  par_key VARCHAR,
# 13  id_cliente INTEGER,
# 14  policyexecutionid VARCHAR,
# 15  siisa_subsectorLaboral INTEGER,
# 16  siisa_montoMorasBCRA INTEGER,
# 17  siisa_cantMorasBCRA INTEGER,
# 18  siisa_relDepMeses INTEGER,
# 19  veraz_score INTEGER,
# 20  siisa_sesModelo INTEGER,
# 21  siisa_consultasAno INTEGER,
# 22  siisa_sectorLaboral VARCHAR,
# 23  siisa_ingreso FLOAT,
# 24  siisa_compromiso FLOAT,
# 25  siisa_maxBCRA24m INTEGER,
# 26  siisa_score INTEGER,
# 27  siisa_scorePoblacion INTEGER,
# 28  siisa_maxBCRA12mi INTEGER,
# 29  siisa_cantMoras INTEGER,
# 30  siisa_maxBCRA6m INTEGER,
# 31  siisa_consultasSeisMeses INTEGER,
# 32  siisa_sesCat INTEGER,
# 33  siisa_consultasDosAno INTEGER,
# 34  siisa_consultasTresMeses INTEGER,
# 35  siisa_consultasMes INTEGER,


for row in csvreader:
    codigo = string_to_int(row[4])
    id_credito = string_to_int(row[5])
    monto = string_to_float(row[6])
    id_cliente = string_to_int(row[13])
    siisa_montoMorasBCRA = string_to_int(row[16])
    siisa_cantMorasBCRA = string_to_int(row[17])
    siisa_relDepMeses = string_to_int(row[18])
    veraz_score = string_to_int(row[19])
    siisa_sesModelo = string_to_int(row[20])
    siisa_consultasAno = string_to_int(row[21])
    siisa_ingreso = string_to_float(row[23])
    siisa_compromiso = string_to_float(row[24])
    siisa_maxBCRA24m = string_to_float(row[25])
    siisa_score  = string_to_int(row[26])
    siisa_scorePoblacion = string_to_int(row[27])
    siisa_maxBCRA12mi= string_to_int(row[28])
    siisa_cantMoras = string_to_int(row[29])
    siisa_maxBCRA6m = string_to_int(row[30])
    siisa_consultasSeisMeses = string_to_int(row[31])
    siisa_sesCat = string_to_int(row[32])
    siisa_consultasDosAno = string_to_int(row[33])
    siisa_consultasTresMeses = string_to_int(row[34])
    siisa_consultasMes = string_to_int(row[35])


    # La interpolacion la hacemos porque conozco que el CSV viene de buena fuente
    sql = """
    INSERT INTO creditos
    (
id_credito, tdoc, ndoc, fechainforme, fliquidacion, codigo,
monto, sucursal, nombre, recibo, clase_plan, pkey_job, par_key, id_cliente,
policyexecutionid, siisa_subsectorLaboral, siisa_montoMorasBCRA,
siisa_cantMorasBCRA, siisa_relDepMeses, veraz_score, siisa_sesModelo, siisa_consultasAno,
siisa_sectorLaboral, siisa_ingreso, siisa_compromiso, siisa_maxBCRA24m,
siisa_score, siisa_scorePoblacion, siisa_maxBCRA12mi, siisa_cantMoras, siisa_maxBCRA6m,
siisa_consultasSeisMeses, siisa_sesCat, siisa_consultasDosAno,
siisa_consultasTresMeses, siisa_consultasMes
    )
    VALUES
    (
    '%s', NULL, NULL, NULL, NULL, %s,
    %s, '%s', '%s', '%s', '%s', '%s', '%s', %s,
    '%s', '%s', %s,
    %s, %s, %s, %s, %s,
    '%s', %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s,
    %s, %s
    )
    """ % (
        id_credito, codigo,
        monto, row[7], row[8], row[9], row[10], row[11], row[12], id_cliente,
        row[14], row[15], siisa_montoMorasBCRA,
        siisa_cantMorasBCRA, siisa_relDepMeses, veraz_score, siisa_sesModelo, siisa_consultasAno,
        row[22], siisa_ingreso, siisa_compromiso, siisa_maxBCRA24m,
        siisa_score, siisa_scorePoblacion, siisa_maxBCRA12mi, siisa_cantMoras, siisa_maxBCRA6m,
        siisa_consultasSeisMeses, siisa_sesCat, siisa_consultasDosAno,
        siisa_consultasTresMeses, siisa_consultasMes
    )
    # print(sql)
    cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()
