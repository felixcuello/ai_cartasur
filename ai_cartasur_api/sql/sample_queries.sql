SELECT
  cl.fnac,
  cl.sexo,
  cl.ingreso_neto,
  cl.fecha_alta_laboral,
  cl.tipolaboral,
  cl.metal,
  cl.operaciones,
  cl.refines,
  cl.peor_atraso_hist,
  cl.juicios_cancelados,
  cl.apto_venta_en_caja,
  count(*)
FROM creditos cr
INNER JOIN clientes cl ON cr.id_cliente = cl.id_cliente
GROUP BY
  cl.fnac,
  cl.sexo,
  cl.ingreso_neto,
  cl.fecha_alta_laboral,
  cl.tipolaboral,
  cl.metal,
  cl.operaciones,
  cl.refines,
  cl.peor_atraso_hist,
  cl.juicios_cancelados,
  cl.apto_venta_en_caja;
