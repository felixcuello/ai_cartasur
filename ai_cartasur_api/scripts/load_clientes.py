# ==========================================================================
#   Carga los clientes en el postgres
# ==========================================================================
import os
import csv
import psycopg2

conn = psycopg2.connect("host={} dbname={} user={} password={}".
                        format(
                            os.environ['POSTGRES_HOST'],
                            os.environ['POSTGRES_DB'],
                            os.environ['POSTGRES_USER'],
                            os.environ['POSTGRES_PASSWORD']
                        ))

clientes = open('/data/clientes_up.csv')
csvreader = csv.reader(clientes, delimiter='|')
next(csvreader) # saltear el header

cursor = conn.cursor()
cursor.execute("DELETE FROM clientes;")

def string_to_float(string):
    if string == '':
        return 'NULL'
    else:
        return float(string.replace(",", "."))

def string_to_int(string):
    if string == '':
        return 'NULL'
    else:
        return int(string_to_float(string))

def string_or_null(string):
    if(string == '' or string == None or string == 'NULL'):
        return "NULL"
    else:
        return "'%s'" % (string)

#  0 id_cliente INTEGER PRIMARY KEY,
#  1 tdoc VARCHAR,
#  2 nrodoc VARCHAR,
#  3 sexo VARCHAR,
#  4 falta TIMESTAMP WITHOUT TIME ZONE,
#  5 fnac TIMESTAMP WITHOUT TIME ZONE,
#  6 ingreso_neto INTEGER,
#  7 fecha_alta_laboral TIMESTAMP WITHOUT TIME ZONE,
#  8 sucursal VARCHAR,
#  9 provincia_pero VARCHAR,
# 10 cod_postal_per VARCHAR,
# 11 tipolaboral VARCHAR,
# 12 metal VARCHAR,
# 13 operaciones INTEGER,
# 14 refines INTEGER,
# 15 peor_atraso_hist FLOAT,
# 16 juicios_cancelados VARCHAR,
# 17 apto_venta_en_caja VARCHAR

for row in csvreader:
    ingreso_neto = string_to_int(row[6])
    operaciones = string_to_int(row[13])
    refines = string_to_int(row[14])
    peor_atraso_hist = string_to_float(row[15])
    fecha_alta_laboral = string_or_null(row[7])

    # La interpolacion la hacemos porque conozco que el CSV viene de buena fuente
    sql = """
    INSERT INTO clientes
    (
      id_cliente, tdoc, nrodoc, sexo,
      falta, fnac, ingreso_neto, fecha_alta_laboral,
      sucursal, provincia_pero, cod_postal_per,
      tipolaboral, metal, operaciones, refines,
      peor_atraso_hist, juicios_cancelados, apto_venta_en_caja
    )
    VALUES
    (
    '%s', NULL, NULL, '%s',
    '%s', '%s', %s, %s,
    '%s', '%s', '%s',
    '%s', '%s', %s, %s,
    %s, '%s', '%s'
    )
    """ % (row[0], row[3],
           row[4], row[5], ingreso_neto, fecha_alta_laboral,
           row[8], row[9], row[10],
           row[11], row[12], operaciones, peor_atraso_hist,
           peor_atraso_hist, row[16], row[17])

    cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()
