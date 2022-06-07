# ==========================================================================
#   Carga las cuotas en el postgres
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

cuotas = open('/data/cuotas_up.csv')
csvreader = csv.reader(cuotas, delimiter='|')
next(csvreader) # saltear el header

cursor = conn.cursor()
cursor.execute("DELETE FROM cuotas;")

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
    id_credito = string_to_int(row[0])
    id_cuota_credito = string_to_int(row[1])
    nro_cuota = string_to_int(row[2])
    fvto = timestamp_or_null(row[3])
    capital = string_to_float(row[4])
    interes = string_to_float(row[5])

    # La interpolacion la hacemos porque conozco que el CSV viene de buena fuente
    sql += """
    INSERT INTO cuotas
    (id_credito, id_cuota_credito, nro_cuota, fvto, capital, interes)
    VALUES
    (%s, %s, %s, %s, %s, %s);
    """ % (id_credito, id_cuota_credito, nro_cuota, fvto, capital, interes)
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
