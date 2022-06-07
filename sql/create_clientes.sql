-- Tabla de clientes según CSV
CREATE TABLE clientes (
  id_cliente INTEGER PRIMARY KEY,
  tdoc VARCHAR,
  nrodoc VARCHAR,
  sexo VARCHAR,
  falta TIMESTAMP WITHOUT TIME ZONE,
  fnac TIMESTAMP WITHOUT TIME ZONE,
  ingreso_neto INTEGER,
  fecha_alta_laboral TIMESTAMP WITHOUT TIME ZONE,
  sucursal VARCHAR,
  provincia_pero VARCHAR,
  cod_postal_per VARCHAR,
  tipolaboral VARCHAR,
  metal VARCHAR,
  operaciones INTEGER,
  refines INTEGER,
  peor_atraso_hist FLOAT,
  juicios_cancelados VARCHAR,
  apto_venta_en_caja VARCHAR
);

CREATE INDEX id_cliente_idx ON public.clientes USING btree (id_cliente);
