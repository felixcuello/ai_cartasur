-- Tabla de pagos según CSV
CREATE TABLE pagos (
  id_credito INTEGER,
  nro_cuota INTEGER NOT NULL,
  fpago TIMESTAMP NOT NULL,
  capital FLOAT,
  interes FLOAT,
  CONSTRAINT fk_id_credito FOREIGN KEY(id_credito) REFERENCES creditos(id_credito)
);
