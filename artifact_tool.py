import pandas as pd
import numpy as np

from functools import lru_cache, partial
from types import SimpleNamespace

import ceam_inputs
from gbd_mapping import covariates
from vivarium_gbd_access import gbd


class HDF_Path_Parser():
    def __init__(self):
        self.root = {}

    def add(self, path):
        nodes = path.split("/")[1:]
        level = self.root
        while len(nodes) > 0:
            current_node = nodes.pop(0)
            if current_node not in level:
                level[current_node] = {}
            level = level[current_node]
        level['path'] = path

    def to_namespace(self):
        return self._dict_to_namespace(self.root)

    def _dict_to_namespace(self, root):
        for key in root:
            if key == 'path':
                continue
            root[key] = self._dict_to_namespace(root[key])
        return SimpleNamespace(**root)


class ArtifactTool():

    def __init__(self, path):
        self._path = path
        self._hdf = pd.HDFStore(path)
        self._str = None
        self._parse_paths()
        self._country = self._hdf.get("/dimensions/full_space").location.loc[0]
        self._gbd_location_id = int(gbd.get_location_ids().query('location_name == "' + self._country + '"').location_id)
        self.covariates = self._create_covariates()

    def _parse_paths(self):
        """ Parse the paths of the hdf in order to:
            - create a string representing the hdf
            - collect each cause and risk
            - store path information in the AT
        """
        self._causes = set()
        self._risks = set()

        self._str = "HDF: " + self._path + "\n"
        self._str += "---Table Map---\n"

        self._table_paths = []

        path_parser = HDF_Path_Parser()

        for path, _ in self._hdf.items():
            path_parser.add(path)
            self._table_paths.append(path)

            path_list = path.split('/')
            path_list = path_list[1:]

            # Collect risks and causes
            if path_list[0] == 'cause':
                self._causes.add(path_list[1])
            if path_list[0] == "risk_factor":
                self._risks.add(path_list[1])

            self._str += str(path) + "\n"

        self.paths = path_parser.to_namespace()

    def _create_covariates(self):
        covars = covariates.to_dict()
        covars = {c: partial(self._get_covariate, covars[c]['gbd_id']) for c in covars}
        return SimpleNamespace(**covars)

    def _get_covariate(self, covariate_ids):
        return gbd.get_covariate_estimates([covariate_ids], self._gbd_location_id)

    @property
    def risks(self):
        return self._risks

    @property
    def causes(self):
        return self._causes

    @property
    def location(self):
        return self._country

    def __str__(self):
        return self._str

    def __del__(self):
        self._hdf.close()

    def get(self, path):
        assert path in self._table_paths, "Path: " + path + " is invalid for HDF: " + self._path
        return self._hdf.get(path)

    @lru_cache(maxsize=32)
    def population_for_year_with_age_limit(self, year: int=2016, lower: float=0, upper: float=5):
        table = self._get_table_for_year_with_age_limit('/population/structure', year, lower, upper)
        return table.population.sum() / 2

    @lru_cache(maxsize=32)
    def population_for_year(self, year: int=2016):
        return self.population_for_year_with_age_limit(year, 0, 1000)

    @lru_cache(maxsize=32)
    def deaths_for_year_with_age_limit(self, year: int=2016, lower: float=0, upper: float=5):
        table = self._get_table_for_year_with_age_limit('/cause/all_causes/death', year, lower, upper)
        return table.value.sum() / 1000 / 2

    @lru_cache(maxsize=32)
    def deaths_for_year(self, year: int =2016):
        return self.deaths_for_year_with_age_limit(year, 0, 1000)

    @lru_cache(maxsize=32)
    def live_births_for_year(self, year: int=2016):
        table = self._hdf.get('/covariate/live_births_by_sex/estimate')
        table = table[table.year == year]
        return table.mean_value.sum() / 2

    @lru_cache(maxsize=32)
    def crude_birth_rate_for_year(self, year: int=2016):
        live_birth_rate = self.live_births_for_year(year)
        population_size = self.population_for_year(year)
        return live_birth_rate / population_size * 1000

    @lru_cache(maxsize=32)
    def child_mortality_rate_for_year(self, year: int =2016):
        deaths_under_5 = self.deaths_for_year_with_age_limit(year, 0, 5)
        live_birth_rate = self.live_births_for_year(year)
        return deaths_under_5 / live_birth_rate * 1000

    @lru_cache(maxsize=32)
    def exposure_rates_by_year_with_age_limit(self, risk_factor: str, year: int=2016, lower: int=0, upper: int=5):
        assert risk_factor in self._risks, "risk_factor is not in the Artifact"

        table = self._get_table_for_year_with_age_limit('/risk_factor/' + risk_factor + '/exposure', year, lower, upper)
        table = self.reduce_draws(table)
        table = self.append_population(table)

        exposed = table.value_mean * table.population

        groups = table.groupby(['parameter']).groups
        numerator = [exposed[groups[risk]].sum() for risk in groups]
        denominator = [table.population[groups[risk]].sum() for risk in groups]

        cat_map = {cat: ceam_inputs.risk_factors[risk_factor].levels[cat] for cat in table.parameter.unique()}

        n_rows = len(groups)
        results = self._default_result_table(year, n_rows)
        results['risk'] = [risk_factor] * n_rows
        results['parameter'] = pd.Series(list(groups.keys())).map(cat_map)
        results['exposure_rate'] = [numerator[i] / denominator[i] for i in range(len(numerator))]
        return results

    @lru_cache(maxsize=32)
    def relative_risk_by_year_with_age_limit(self, risk_factor: str, year: int=2016, lower: float=0, upper: float=5):
        assert risk_factor in self._risks, "risk_factor is not in the Artifact"

        table = self._get_table_for_year_with_age_limit('/risk_factor/' + risk_factor + '/relative_risk', year, lower, upper)
        table = self.reduce_draws(table)
        table = self.append_population(table)

        weighted_risk = table.population * table.value_mean

        groups = table.groupby(['cause', 'parameter']).groups
        numerator = [weighted_risk[groups[risk]].sum() for risk in groups]
        denominator = [table.population[groups[risk]].sum() for risk in groups]

        cat_map = {cat: ceam_inputs.risk_factors[risk_factor].levels[cat] for cat in table.parameter.unique()}

        n_rows = len(groups)
        results = self._default_result_table(year, n_rows)
        causes, parameters = zip(*list(groups.keys()))
        results['risk'] = [risk_factor] * n_rows
        results['parameter'] = pd.Series(parameters).map(cat_map)
        results['cause'] = causes
        results['relative_risk'] = [numerator[i] / denominator[i] for i in range(len(numerator))]
        return results

    def SEV_for_year_with_age_limit(self, risk_factor: str, year: int=2016, lower: float=0, upper: float=5):
        # GBD Uses strict age bins for calculating DBF and NEBF
        if risk_factor == "discontinued_breastfeeding":
            lower = 0.5
            upper = 3
        if risk_factor == "non_exclusive_breastfeeding":
            lower = 0.04
            upper = 1

        exposure_table = self.exposure_rates_by_year_with_age_limit(risk_factor, year, lower, upper)
        rr_table = self.relative_risk_by_year_with_age_limit(risk_factor, year, lower, upper)
        table = rr_table.sort_values(by=['cause', 'parameter'])
        table['exposure'] = exposure_table.exposure_rate.tolist() * len(rr_table.cause.unique())

        numerator = table.relative_risk * table.exposure

        groups = table.groupby(['cause']).groups
        numerator = [numerator[groups[cause]].sum() - 1 for cause in groups]
        denominator = [table.relative_risk[groups[cause]].max() - 1 for cause in groups]

        n_rows = len(groups)
        results = self._default_result_table(year, n_rows)
        results['risk'] = [risk_factor] * n_rows
        results['cause'] = list(groups.keys())
        results['SEV'] = [numerator[i] / denominator[i] for i in range(len(numerator))]
        return results

    def PAF_for_year_with_age_limit(self, cause: str, year: int=2016, lower: float=0, upper: float=5):
        assert cause in self._causes, "cause is not in the Artifact"
        assert cause != 'all_causes', "all_causes does not have a PAF"

        table = self._get_table_for_year_with_age_limit('/cause/' + cause + '/population_attributable_fraction', year, lower, upper)
        table = self.reduce_draws(table)
        table = self.append_population(table)

        weighted_paf = table.value_mean * table.population

        groups = table.groupby(by=["risk"]).groups
        numerator = [weighted_paf[groups[risk]].sum() for risk in groups]
        denominator = [table.population[groups[risk]].sum() for risk in groups]

        n_rows = len(groups)
        results = self._default_result_table(year, n_rows)
        results['cause'] = [cause] * n_rows
        results['risk'] = list(groups.keys())
        results['PAF'] = [numerator[i] / denominator[i] for i in range(len(numerator))]
        return results

    def CSMR_for_year_with_age_limit(self, cause: str, year: int=2016, lower: float=0, upper: float=5):
        assert cause in self._causes, "cause is not in the Artifact"

        table = self._get_table_for_year_with_age_limit('/cause/' + cause + '/cause_specific_mortality', year, lower, upper)
        table = table[table.sex == "Both"]
        table = self.reduce_draws(table)
        table = self.append_population(table)

        n_rows = 1
        results = self._default_result_table(year, n_rows)
        results['cause'] = [cause] * n_rows
        results['CSMR'] = [(table.value_mean * table.population).sum() / table.population.sum()]
        return results

    def incidence_for_year_with_age_limit(self, cause: str, year: int=2016, lower: float=0, upper: float=5):
        assert cause in self._causes, "cause is not in the Artifact"

        table = self._get_table_for_year_with_age_limit('/cause/' + cause + '/incidence', year, lower, upper)
        table = table[table.sex == "Both"]
        table = self.reduce_draws(table)
        table = self.append_population(table)

        n_rows = 1
        results = self._default_result_table(year, n_rows)
        results['cause'] = [cause] * n_rows
        results['incidence'] = [(table.value_mean * table.population).sum() / table.population.sum()]
        return results

    def reduce_draws(self, table: pd.DataFrame, val_col: str="value"):
        """Creates a DataFrame with mean and CI values obtained across draws.

        Parameters
        ----------
        table:
            A pandas DataFrame that contains a "draw" column
        col_name:
            The name of the column inside table that the mean and CI values should
            be computed from. The column should contain numeric values.

        Returns
        -------
        A table that summarizes key statistical values for a specific column
        """
        assert "draw" in table.columns, "Table does not have a column named draw"

        drawless_table = table.query('draw == 0')

        # create identifiers for each row, independent of draws
        columns = drawless_table.columns.tolist()
        columns = [c for c in columns if c not in ['draw', val_col]]

        # turn the identifiers into strings
        identifiers = []
        for index, row in drawless_table.sort_values(by=columns).iterrows():
            row_list = row[columns].tolist()
            ID = '-'.join([str(row) for row in row_list])
            identifiers.append(ID)

        # create a table that has draws as rows and identifiers as columns
        table = table.sort_values(by=['draw'] + columns)
        values = table[val_col].values
        values = values.reshape(len(table) // len(identifiers), len(identifiers))
        value_df = pd.DataFrame(values, columns=identifiers)

        # remove the values column from our drawless table and add columns for the
        # stats we want
        result_df = drawless_table[columns].sort_values(by=columns)
        result_df[val_col + "_mean"] = [value_df[col].values.mean() for col in identifiers]
        result_df['lower 2.5'] = [np.percentile(value_df[col].values, 2.5) for col in identifiers]
        result_df['upper 97.5'] = [np.percentile(value_df[col].values, 97.5) for col in identifiers]
        result_df = result_df.reset_index(drop=True)

        return result_df

    def append_population(self, table: pd.DataFrame):
        """ Appends a new column with population data based on a rows Maps data
            on age, sex and year.

        Parameters
        ----------
        table:
            A pandas DataFrame that contains "age", "sex" and "year" columns

        Returns
        -------
        table with a column named population appended to it.
        """
        assert all([col_name in table.columns for col_name in ["age", "year", "sex"]]), "table does not have all the required columns"

        pop_table = self._hdf.get('/population/structure')
        # Set each column to a str so we can hash them
        table_age = table.age.astype(str)
        table_year = table.year.astype(str)
        table_sex = table.sex.astype(str)
        pop_age = pop_table.age.astype(str)
        pop_year = pop_table.year.astype(str)
        pop_sex = pop_table.sex.astype(str)

        table_hash = (table_age + table_year + table_sex)
        pop_table['hash'] = (pop_age + pop_year + pop_sex)

        @lru_cache(maxsize=256)
        def hash_to_pop(hash_key):
            return float(pop_table[pop_table.hash == hash_key].population.values)
        table['population'] = table_hash.map(hash_to_pop)

        pop_table = pop_table.drop(columns=['hash'])
        return table

    def _get_table_for_year_with_age_limit(self, path, year, lower, upper):
        """

        Parameters
        ----------
        path:
            A valid path in self._hdf.
        year:
            An integer representing the year of the results
        lower:
            A lower bound on age
        upper: An upper bound on age

        Returns
        -------
        A default results table.
        """
        assert path in self._table_paths, "The table: " + str(path) + " does not exist in the hdf: " + str(self._path)

        table = self._hdf.get(path)
        table = table[table.year == year]
        table = table[table.age <= upper]
        table = table[table.age >= lower]
        return table

    def _default_result_table(self, year, n_rows):
        """ Returns a default results table used to format results.

        Parameters
        ----------
        year:
            An integer representing the year of the results
        n_rows:
            A non-negative integer representing the number of rows for the results

        Returns
        -------
        A default results table.
        """
        assert n_rows >= 0

        results = pd.DataFrame([year] * n_rows, columns=['year'])
        results['location'] = [self._country] * n_rows
        results['sex'] = ["Both"] * n_rows
        return results
