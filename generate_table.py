import pandas as pd
from artifact_tool import ArtifactTool
import glob


artifact_paths = glob.glob('/share/scratch/users/abie/bfp_*.hdf')
artifact_paths.remove('/share/scratch/users/abie/bfp_sierra_leone.hdf')
artifact_paths.remove('/share/scratch/users/abie/bfp_sierra-leone.hdf')
artifact_paths.remove('/share/scratch/users/abie/bfp_Chad.hdf')
artifact_paths.remove('/share/scratch/users/abie/bfp_2.hdf')

country_dict = {}
for path in artifact_paths:
    print(path)
    at = ArtifactTool(path)
    stat_dict = {}

    stat_dict['population'] = at.population_for_year(2016)
    stat_dict['population under 5'] = at.population_for_year_with_age_limit(2016, 0, 5)
    stat_dict['crude birth rate'] = at.crude_birth_rate_for_year(2016)
    stat_dict['childhood mortality rate'] = at.child_mortality_rate_for_year(2016)

    # SEV's
    sev = at.SEV_all_risk_factors_for_year_with_age_limit(2016, 0, 5)
    for i, key in enumerate("SEV for: " + sev.risk + "/" + sev.cause):
        stat_dict[key] = sev.SEV.loc[i]
    # PAF's
    paf = at.PAF_all_causes_for_year_with_age_limit(2016, 0, 5)
    for i, key in enumerate("PAF for: " + paf.risk + "/" + paf.cause):
        stat_dict[key] = paf.PAF.loc[i]
    # CSMR
    csmr = at.CSMR_all_causes_for_year_with_age_limit(2016, 0, 5)
    for i, key in enumerate("CSMR for: " + csmr.cause):
        stat_dict[key] = csmr.CSMR.loc[i]
    # incidence
    incidence = at.incidence_all_causes_for_year_with_age_limit(2016, 0, 5)
    for i, key in enumerate("incidence for: " + incidence.cause):
        stat_dict[key] = incidence.incidence.loc[i]

    ##### Covariates
    stat_dict['HAQI'] = at.covariates.healthcare_access_and_quality_index().query('year_id == 2016').mean_value.values[0]
    stat_dict['ANC1'] = at.covariates.antenatal_care_1_visit_coverage_proportion().query('year_id == 2016').mean_value.values[0]
    stat_dict['ANC4'] = at.covariates.antenatal_care_4_visits_coverage_proportion().query('year_id == 2016').mean_value.values[0]
    stat_dict['urbancity'] = at.covariates.urbanicity().query('year_id == 2016').mean_value.values[0]
    stat_dict['in facility birth rate'] = at.covariates.in_facility_delivery_proportion().query('year_id == 2016').mean_value.values[0]
    stat_dict['LDI'] = at.covariates.ldi_income_per_capita().query('year_id == 2016').mean_value.values[0]
    stat_dict['SDI'] = at.covariates.socio_demographic_index().query('year_id == 2016').mean_value.values[0]
    stat_dict['ten year lag distributed energy per capita'] = at.covariates.ten_year_lag_distributed_energy_per_capita().query('year_id == 2016').mean_value.values[0]
    stat_dict['SBA'] = at.covariates.skilled_birth_attendance_proportion().query('year_id == 2016').mean_value.values[0]
    stat_dict['SEV unsafe water'] = at.covariates.sev_unsafe_water().query('year_id == 2016').mean_value.values[0]
    stat_dict['SEV unsafe sanitation'] = at.covariates.sev_unsafe_sanitation().query('year_id == 2016').mean_value.values[0]
    stat_dict['no access to handwashing facility'] = at.covariates.no_access_to_handwashing_facility().query('year_id == 2016').mean_value.values[0]
    stat_dict['education years per capita'] = at.covariates.education_years_per_capita().query('year_id == 2016').mean_value.values[0]

    # Save the dictionary
    country_dict[path] = stat_dict
    del(at)
table = pd.DataFrame(country_dict)
table.to_csv('table.csv')
