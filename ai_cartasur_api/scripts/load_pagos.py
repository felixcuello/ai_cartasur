# ==========================================================================
#   Carga las pagos en el postgres
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

pagos = open('/data/pagos_up.csv')
csvreader = csv.reader(pagos, delimiter='|')
next(csvreader) # saltear el header

cursor = conn.cursor()
cursor.execute("DELETE FROM pagos;")

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

def timestamp_or_null(string):
    if(string == '' or string == None or string == 'NULL'):
        return "NULL"
    else:
        return "'%s'" % (string)

i = 0
sql = ""
for row in csvreader:
    #ID_CREDITO|NRO_CUOTA|ID_CUOTA_CREDITO|FPAGO|CAPITAL|INTERES
    id_credito = string_to_int(row[0])
    nro_cuota = string_to_int(row[1])
    id_cuota_credito = string_to_int(row[2])
    fpago = timestamp_or_null(row[3])
    capital = string_to_float(row[4])
    interes = string_to_float(row[5])

    # La interpolacion la hacemos porque conozco que el CSV viene de buena fuente
    sql += """
    INSERT INTO pagos
    (id_credito, id_cuota_credito, nro_cuota, fpago, capital, interes)
    VALUES
    (%s, %s, %s, %s, %s, %s);
    """ % (id_credito, id_cuota_credito, nro_cuota, fpago, capital, interes)
    i += 1
    if i % 100000 == 0:
        print("{}".format(i))
        cursor.execute(sql)
        conn.commit()
        sql = ""

cursor.execute(sql)
conn.commit()
cursor.close()
conn.close()
