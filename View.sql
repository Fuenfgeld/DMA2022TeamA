DROP VIEW IF EXISTS v_encounters_plus;
CREATE VIEW v_encounters_plus AS 
SELECT
   encounter_procedures.Id,
   encounter_procedures.DATASET_ORIGIN,
   encounter_procedures.encounter_START,
   encounter_procedures.encounter_STOP,
   encounter_procedures.PATIENT_Id,
   encounter_procedures.PAYER_Id,
   encounter_procedures.payer_START_YEAR,
   encounter_procedures.payer_END_YEAR,
   encounter_procedures.payer_OWNERSHIP,
   encounter_procedures.ENCOUNTERCLASS,
   encounter_procedures.encounter_CODE,
   encounter_procedures.encounter_DESCRIPTION,
   encounter_procedures.encounter_REASONCODE,
   encounter_procedures.encounter_REASONDESCRIPTION,
   encounter_procedures.condition_START,
   encounter_procedures.condition_STOP,
   encounter_procedures.condition_CODE,
   encounter_procedures.condition_DESCRIPTION,
   encounter_procedures.immunization_DATE,
   encounter_procedures.immunization_CODE,
   encounter_procedures.immunizations_DESCRIPTION,
   encounter_procedures.procedure_DATE,
   encounter_procedures.procedure_CODE,
   encounter_procedures.procedure_DESCRIPTION,
   encounter_procedures.procedure_REASONCODE,
   encounter_procedures.procedure_REASONDESCRIPTION,
   encounter_procedures.BASE_ENCOUNTER_COST,
   encounter_procedures.BASE_IMMUNIZATION_COST,
   encounter_procedures.BASE_PROCEDURE_COST,
   FROM
   (
      SELECT
         procedures.DATE AS procedure_DATE,
         procedures.CODE AS procedure_CODE,
         procedures.DESCRIPTION AS procedure_DESCRIPTION,
         procedures.REASONCODE AS procedure_REASONCODE,
         procedures.REASONDESCRIPTION AS procedure_REASONDESCRIPTION,
         procedures.BASE_COST AS BASE_PROCEDURE_COST, 
      FROM
         (
            SELECT
               encounters_conditions.Id,
               encounters_conditions.DATASET_ORIGIN,
               encounters_conditions.encounter_START,
               encounters_conditions.encounter_STOP,
               encounters_conditions.PATIENT_Id,
               encounters_conditions.PAYER_Id,
               encounters_conditions.payer_START_YEAR,
               encounters_conditions.payer_END_YEAR,
               encounters_conditions.payer_OWNERSHIP,
               encounters_conditions.ENCOUNTERCLASS,
               encounters_conditions.encounter_CODE,
               encounters_conditions.encounter_DESCRIPTION,
               encounters_conditions.encounter_REASONCODE,
               encounters_conditions.encounter_REASONDESCRIPTION,
               encounters_conditions.condition_START,
               encounters_conditions.condition_STOP,
               encounters_conditions.condition_CODE,
               encounters_conditions.condition_DESCRIPTION,
               encounters_conditions.BASE_ENCOUNTER_COST,
               FROM
               (
                  SELECT
                     encounters_payer_transitions.Id,
                     encounters_payer_transitions.DATASET_ORIGIN,
                     encounters_payer_transitions.encounter_START,
                     encounters_payer_transitions.encounter_STOP,
                     encounters_payer_transitions.PATIENT_Id,
                     encounters_payer_transitions.PAYER_Id,
                     encounters_payer_transitions.payer_START_YEAR,
                     encounters_payer_transitions.payer_END_YEAR,
                     encounters_payer_transitions.payer_OWNERSHIP,
                     encounters_payer_transitions.ENCOUNTERCLASS,
                     encounters_payer_transitions.encounter_CODE,
                     encounters_payer_transitions.encounter_DESCRIPTION,
                     encounters_payer_transitions.encounter_REASONCODE,
                     encounters_payer_transitions.encounter_REASONDESCRIPTION,
                     conditions.START AS condition_START,
                     conditions.STOP AS condition_STOP,
                     conditions.CODE AS condition_CODE,
                     conditions.DESCRIPTION AS condition_DESCRIPTION,
                     FROM
                     (
                        SELECT
                           encounters.Id,
                           encounters.DATASET_ORIGIN,
                           encounters.START AS encounter_START,
                           encounters.STOP AS encounter_STOP,
                           encounters.PATIENT_Id,
                           encounters.PAYER_Id,
                           payer_transitions.START_YEAR AS payer_START_YEAR,
                           payer_transitions.END_YEAR AS payer_END_YEAR,
                           payer_transitions.OWNERSHIP AS payer_OWNERSHIP,
                           encounters.ENCOUNTERCLASS,
                           encounters.CODE AS encounter_CODE,
                           encounters.DESCRIPTION AS encounter_DESCRIPTION,
                           encounters.REASONCODE AS encounter_REASONCODE,
                           encounters.REASONDESCRIPTION AS encounter_REASONDESCRIPTION,
                           encounters.BASE_ENCOUNTER_COST,
                        FROM
                           encounters 
                           LEFT JOIN
                              payer_transitions 
                              ON payer_transitions.PAYER_ID = encounters.PAYER_Id 
                              AND payer_transitions.PATIENT_Id = encounters.PATIENT_Id 
                     )
                     encounters_payer_transitions 
                     LEFT JOIN
                        conditions 
                        ON conditions.ENCOUNTER_Id = encounters_payer_transitions.Id 
                        AND conditions.ENCOUNTER_DSO = encounters_payer_transitions.DATASET_ORIGIN 
                        AND conditions.PATIENT_Id = encounters_payer_transitions.PATIENT_Id 
               )
               encounters_conditions 
               LEFT JOIN
                  immunizations 
                  ON immunizations.ENCOUNTER_Id = encounters_conditions.Id 
                  AND immunizations.ENCOUNTER_DSO = encounters_conditions.DATASET_ORIGIN 
                  AND immunizations.PATIENT_Id = encounters_conditions.PATIENT_Id 
         )
         encounter_immunizations 
         LEFT JOIN
            procedures 
            ON procedures.ENCOUNTER_Id = encounter_immunizations.Id 
            AND procedures.ENCOUNTER_DSO = encounter_immunizations.DATASET_ORIGIN 
            AND procedures.PATIENT_Id = encounter_immunizations.PATIENT_Id 
   )
   encounter_procedures 
   LEFT JOIN
      medications 
      ON medications.ENCOUNTER_Id = encounter_procedures.Id 
      AND medications.ENCOUNTER_DSO = encounter_procedures.DATASET_ORIGIN 
      AND medications.PATIENT_ID = encounter_procedures.PATIENT_Id 
      AND medications.PAYER_ID = encounter_procedures.PAYER_Id ;
