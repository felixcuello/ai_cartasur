-- Incluyendo cuotas
-- Esta query es TAN lenta para la cantidad de datos que no la puedo correr.
-- La dejo como ejemplo de cómo sacar el agrupamiento por cantidad de créditos Y cantidad de cuotas.

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
  count(*) AS cantidad_creditos,
  COALESCE(cu.total_cuotas, 0) AS total_cuotas
--  ,cr.id_credito
FROM creditos cr
INNER JOIN clientes cl ON cl.id_cliente = cl.id_cliente
LEFT JOIN (
  SELECT    id_credito,
            COUNT(*) AS total_cuotas
  FROM      cuotas
  GROUP BY  id_credito
) cu ON cr.id_credito = cu.id_credito
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
  cl.apto_venta_en_caja,
  cu.total_cuotas
--  ,cr.id_credito
-- HAVING total_cuotas > 5
-- LIMIT 10
;
