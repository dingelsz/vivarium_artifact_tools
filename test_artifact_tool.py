from artifact_tool import *

# List of methods in the AT
#[func for func in dir(at) if func[0:2] != "__"]

at = ArtifactTool('/Users/Zach/Projects/IHME/bfp_nigeria.hdf')

def test_population_by_year():
    assert at.get_population_for_year(2016) == at._hdf.get('/population/structure').query('year == 2016 and sex == "Both"').population.sum()

def test_population_by_year_and_age():
    assert at.get_population_for_year_and_age(2016, 0, 5) == at._hdf.get('/population/structure').query('year == 2016 and sex == "Both" and age <= 5').population.sum()

def test_get_deaths_for_year():
    assert at.get_deaths_for_year(2016) == at._hdf.get('/cause/all_causes/death').query('year == 2016 and sex == "Both"').value.sum() / 1000

def test_get_deaths_for_year_and_age():
    assert at.get_deaths_for_year_and_age(2016, 10, 50) == at._hdf.get('/cause/all_causes/death').query('year == 2016 and sex == "Both" and age <= 50 and age >= 10').value.sum() / 1000

def test_get_live_birth_rate():
    assert at.get_live_birth_rate(1995) == at._hdf.get('/covariate/live_births_by_sex/estimate').query('year == 1995').mean_value.sum() / 2

def test_get_crude_birth_rate():
    # crude_birth_rate depends on get_live_birth_rate and
    # get_population_for_year so we can assume this works if they both work.
    pass

def test_get_child_mortality_rate():
    # See test_get_crude_birth_rate
    pass

def test_expsoure_rates_by_year_and_age():
    assert at.get_exposure_rates_by_year_and_age('child_stunting', 2016, 0, 5).rate.sum() == 1

def test_get_relative_risk_by_year_and_age():
    rr_table = at.get_relative_risk_by_year_and_age('child_stunting', 2016, 0, 5)
    assert all(rr_table[rr_table.parameter == 'cat4'].relative_risk == 1)
