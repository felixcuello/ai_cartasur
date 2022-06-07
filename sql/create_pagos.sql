-- Tabla de pagos según CSV
CREATE TABLE pagos (
  id_credito INTEGER,
  id_cuota_credito INTEGER,
  nro_cuota INTEGER NOT NULL,
  fpago TIMESTAMP NOT NULL,
  capital FLOAT,
  interes FLOAT,
  CONSTRAINT fk_unique_cuotas FOREIGN KEY(id_credito, id_cuota_credito) REFERENCES cuotas(id_credito, id_cuota_credito)
);

