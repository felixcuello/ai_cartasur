-- Tabla de cuotas según CSV
CREATE TABLE cuotas (
  id_credito INTEGER,
  id_cuota_credito INTEGER PRIMARY KEY,
  nro_cuota INTEGER NOT NULL,
  fvto TIMESTAMP,
  capital FLOAT,
  interes FLOAT,
  CONSTRAINT fk_id_credito FOREIGN KEY(id_credito) REFERENCES creditos(id_credito)
);

CREATE UNIQUE INDEX index_cuotas ON public.cuotas USING btree (id_credito, id_cuota_credito);
