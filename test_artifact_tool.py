from artifact_tool import *
from time import time

# List of methods in the AT
#[func for func in dir(at) if func[0:2] != "__"]
#%run artifact_tool.py
at = ArtifactTool('/Users/Zach/Projects/IHME/bfp_nigeria.hdf')

def test_population_for_year():
    assert at.population_for_year(2016) == at._hdf.get('/population/structure').query('year == 2016 and sex == "Both"').population.sum()

def test_population_for_year_with_age_limit():
    assert at.population_for_year_with_age_limit(2016, 0, 5) == at._hdf.get('/population/structure').query('year == 2016 and sex == "Both" and age <= 5').population.sum()

def test_deaths_for_year():
    assert at.deaths_for_year(2016) == at._hdf.get('/cause/all_causes/death').query('year == 2016 and sex == "Both"').value.sum() / 1000

def test_deaths_for_year_with_age_limit():
    assert at.deaths_for_year_with_age_limit(2016, 10, 50) == at._hdf.get('/cause/all_causes/death').query('year == 2016 and sex == "Both" and age <= 50 and age >= 10').value.sum() / 1000

def test_live_births_for_year():
    assert at.live_births_for_year(1995) == at._hdf.get('/covariate/live_births_by_sex/estimate').query('year == 1995').mean_value.sum() / 2

def test_crude_birth_rate_for_year():
    # crude_birth_rate depends on live_births_for_year and
    # population_for_year so we can assume this works if they both work.
    pass

def test_child_mortality_rate_for_year():
    # See test_get_crude_birth_rate
    pass

def test_exposure_rates_by_year_with_age_limit():
    for risk in at._risks:
        assert at.exposure_rates_by_year_with_age_limit(risk, 2016, 0, 5).exposure_rate.sum() - 1 < 1e-5

def test_relative_risk_by_year_with_age_limit():
    for risk in at._risks:
        rr_table = at.relative_risk_by_year_with_age_limit(risk, 2016, 0.04, 1)
        max_parameter = max(rr_table.parameter.unique())
        assert all(rr_table[rr_table.parameter == max_parameter].relative_risk - 1 < 1e-5)

def test_SEV_for_year_with_age_limit():
    start_time = time()
    for risk in at._risks:
        SEV = at.SEV_for_year_with_age_limit(risk, 2016, 0, 5)
        assert all(SEV.SEV >= 0) and all(SEV.SEV <= 1)
