-- ============================================
-- Phase 4: Warehouse Reporting Queries
-- ============================================

-- Monthly encounter volume by department
SELECT
    d.year,
    d.month,
    d.month_name,
    dep.dept_name,
    COUNT(*) AS encounters,
    ROUND(AVG(e.los_hours), 1) AS avg_los_hours,
    ROUND(SUM(e.total_charges), 0) AS total_charges,
    SUM(e.inpatient_flag) AS inpatient_count,
    SUM(e.mortality_flag) AS deaths
FROM clinical.fact_encounter_wh e
JOIN clinical.dim_date d ON e.admit_date = d.date_id
JOIN clinical.dim_department dep ON e.dept_id = dep.dept_id
WHERE d.year = 2025
GROUP BY d.year, d.month, d.month_name, dep.dept_name
ORDER BY d.month, dep.dept_name;