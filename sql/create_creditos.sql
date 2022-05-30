-- Tabla de creditos según CSV
CREATE TABLE creditos (
  id_credito INTEGER PRIMARY KEY,
  tdoc VARCHAR,
  ndoc VARCHAR,
  fechainforme date,
  fliquidacion TIMESTAMP WITHOUT TIME ZONE,
  codigo INTEGER,
  monto FLOAT,
  sucursal VARCHAR,
  nombre VARCHAR,
  recibo VARCHAR,
  clase_plan VARCHAR,
  pkey_job VARCHAR,
  par_key VARCHAR,
  id_cliente INTEGER,
  policyexecutionid VARCHAR,
  siisa_subsectorLaboral INTEGER,
  siisa_montoMorasBCRA INTEGER,
  siisa_cantMorasBCRA INTEGER,
  siisa_relDepMeses INTEGER,
  veraz_score INTEGER,
  siisa_sesModelo INTEGER,
  siisa_consultasAno INTEGER,
  siisa_sectorLaboral VARCHAR,
  siisa_ingreso FLOAT,
  siisa_compromiso FLOAT,
  siisa_maxBCRA24m INTEGER,
  siisa_score INTEGER,
  siisa_scorePoblacion INTEGER,
  siisa_maxBCRA12mi INTEGER,
  siisa_cantMoras INTEGER,
  siisa_maxBCRA6m INTEGER,
  siisa_consultasSeisMeses INTEGER,
  siisa_sesCat INTEGER,
  siisa_consultasDosAno INTEGER,
  siisa_consultasTresMeses INTEGER,
  siisa_consultasMes INTEGER,
  CONSTRAINT fk_id_cliente FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente)
);
