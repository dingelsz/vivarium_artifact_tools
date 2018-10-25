from gbd_artifact_tool import *
from gbd_mapping import covariates

class BFP_ArtifactTool(GBD_ArtifactTool):

    def __init__(self, path):
        super().__init__(path)
        self._bfp_parse_paths()
        self._country = self._hdf.get("/dimensions/full_space").location.loc[0]
        self._gbd_location_id = int(gbd.get_location_ids().query('location_name == "' + self._country + '"').location_id)
        self.covariates = self._bfp_covariates()

    def _bfp_parse_paths(self):
        """ Parse the paths for risks and causes
        """
        self._causes = set()
        self._risks = set()

        for path, _ in self._hdf.items():
            path_list = path.split('/')
            # Collect risks and causes
            if path_list[1] == 'cause':
                self._causes.add(path_list[2])
            if path_list[1] == "risk_factor":
                self._risks.add(path_list[2])

        self.risks = SimpleNamespace(**{risk: risk for risk in self._risks})
        self.causes = SimpleNamespace(**{cause: cause for cause in self._causes})

    def _bfp_covariates(self):
        covars = covariates.to_dict()
        covars = {c: partial(gbd.get_covariate_estimates, [covars[c]['gbd_id']], self._gbd_location_id) for c in covars}
        return SimpleNamespace(**covars)

    @property
    def location(self):
        return self._country

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
        exposed_lower = table.lower * table.population
        exposed_upper = table.upper * table.population

        groups = table.groupby(['parameter']).groups
        numerator = [exposed[groups[risk]].sum() for risk in groups]
        numerator_lower = [exposed_lower[groups[risk]].sum() for risk in groups]
        numerator_upper = [exposed_upper[groups[risk]].sum() for risk in groups]
        denominator = [table.population[groups[risk]].sum() for risk in groups]

        cat_map = {cat: ceam_inputs.risk_factors[risk_factor].levels[cat] for cat in table.parameter.unique()}

        n_rows = len(groups)
        results = self._default_result_table(year, n_rows)
        results['risk'] = [risk_factor] * n_rows
        results['parameter'] = pd.Series(list(groups.keys())).map(cat_map)
        results['exposure_rate'] = [numerator[i] / denominator[i] for i in range(len(numerator))]
        results['exposure_rate_lower'] = [numerator_lower[i] / denominator[i] for i in range(len(numerator))]
        results['exposure_rate_upper'] = [numerator_upper[i] / denominator[i] for i in range(len(numerator))]
        return results

    @lru_cache(maxsize=32)
    def relative_risk_by_year_with_age_limit(self, risk_factor: str, year: int=2016, lower: float=0, upper: float=5):
        assert risk_factor in self._risks, "risk_factor is not in the Artifact"

        table = self._get_table_for_year_with_age_limit('/risk_factor/' + risk_factor + '/relative_risk', year, lower, upper)
        table = self.reduce_draws(table)
        table = self.append_population(table)

        weighted_risk = table.population * table.value_mean
        weighted_risk_lower = table.population * table.lower
        weighted_risk_upper = table.population * table.upper

        groups = table.groupby(['cause', 'parameter']).groups
        numerator = [weighted_risk[groups[risk]].sum() for risk in groups]
        numerator_lower = [weighted_risk_lower[groups[risk]].sum() for risk in groups]
        numerator_upper = [weighted_risk_upper[groups[risk]].sum() for risk in groups]
        denominator = [table.population[groups[risk]].sum() for risk in groups]

        cat_map = {cat: ceam_inputs.risk_factors[risk_factor].levels[cat] for cat in table.parameter.unique()}

        n_rows = len(groups)
        results = self._default_result_table(year, n_rows)
        causes, parameters = zip(*list(groups.keys()))
        results['risk'] = [risk_factor] * n_rows
        results['parameter'] = pd.Series(parameters).map(cat_map)
        results['cause'] = causes
        results['relative_risk'] = [numerator[i] / denominator[i] for i in range(len(numerator))]
        results['relative_risk_lower'] = [numerator_lower[i] / denominator[i] for i in range(len(numerator))]
        results['relative_risk_upper'] = [numerator_upper[i] / denominator[i] for i in range(len(numerator))]
        return results

    def SEV_for_year_with_age_limit(self, risk_factor: str, year: int=2016, lower: float=0, upper: float=5):
        # GBD Uses strict age bins for calculating DBF and NEBF
        if risk_factor == "discontinued_breastfeeding":
            lower = 0.5
            upper = 3
        if risk_factor == "non_exclusive_breastfeeding":
            lower = 0.04
            upper = 1
        if risk_factor == "child_stunting":
            lower = 0.5
            upper = 3
        if risk_factor == "child_underweight":
            lower = 0.5
            upper = 3
        if risk_factor == "child_wasting":
            lower = 0.5
            upper = 3

        rr_table = self.relative_risk_by_year_with_age_limit(risk_factor, year, lower, upper)
        exposure_table = self.exposure_rates_by_year_with_age_limit(risk_factor, year, lower, upper)
        exposure_table = exposure_table.sort_values(by=['parameter'])
        table = rr_table.sort_values(by=['cause', 'parameter'])
        table['exposure'] = exposure_table.exposure_rate.tolist() * len(rr_table.cause.unique())
        table['exposure_lower'] = exposure_table.exposure_rate_lower.tolist() * len(rr_table.cause.unique())
        table['exposure_upper'] = exposure_table.exposure_rate_upper.tolist() * len(rr_table.cause.unique())

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

    def SEV_all_risk_factors_for_year_with_age_limit(self, year: int=2016, lower: float=0, upper: float=5):
        tmp_risks = self._risks.copy()
        table = self.SEV_for_year_with_age_limit(tmp_risks.pop(), year, lower, upper)
        for risk_factor in tmp_risks:
            table = table.append(self.SEV_for_year_with_age_limit(risk_factor, year, lower, upper))
        return table.reset_index()

    def PAF_for_year_with_age_limit(self, risk_factor: str, year: int=2016, lower: float=0, upper: float=5):
        assert risk_factor in self._risks, "risk is not in the Artifact"

        exp_table = self.exposure_rates_by_year_with_age_limit(risk_factor, year, lower, upper)
        rr_table = self.relative_risk_by_year_with_age_limit(risk_factor, year, lower, upper)

        table = rr_table
        table['exposure_rate'] = exp_table.exposure_rate.tolist() * len(rr_table.cause.unique())

        product = table.exposure_rate * table.relative_risk
        groups = table.groupby(['cause']).groups
        paf = [(product[groups[cause]].sum() - 1) / product[groups[cause]].sum()  for cause in groups]

        n_rows = len(groups)
        results = self._default_result_table(year, n_rows)
        results['cause'] = table.cause.unique()
        results['risk'] = [risk_factor] * len(results.cause)
        results['PAF'] = paf
        return results

    def PAF_all_risks_for_year_with_age_limit(self, year: int=2016, lower: float=0, upper: float=5):
        tmp_risks = self._risks.copy()
        table = self.PAF_for_year_with_age_limit(tmp_risks.pop(), year, lower, upper)
        for risk in tmp_risks:
            table = table.append(self.PAF_for_year_with_age_limit(risk, year, lower, upper))
        return table.reset_index()

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

    def CSMR_all_causes_for_year_with_age_limit(self, year: int=2016, lower: float=0, upper: float=5):
        tmp_causes = self._causes.copy()
        tmp_causes.remove('all_causes')
        table = self.CSMR_for_year_with_age_limit(tmp_causes.pop(), year, lower, upper)
        for cause in tmp_causes:
            table = table.append(self.CSMR_for_year_with_age_limit(cause, year, lower, upper))
        return table.reset_index()

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

    def incidence_all_causes_for_year_with_age_limit(self, year: int=2016, lower: float=0, upper: float=5):
        tmp_causes = self._causes.copy()
        tmp_causes.remove('all_causes')
        table = self.incidence_for_year_with_age_limit(tmp_causes.pop(), year, lower, upper)
        for cause in tmp_causes:
            table = table.append(self.incidence_for_year_with_age_limit(cause, year, lower, upper))
        return table.reset_index()

    def SEV_unsafe_water_for_year_under5(self, year: int=2016):
        table = at.covariates.sev_unsafe_water()
        table = table[table.year_id == year]
        table = table[table.age_group_id <= 5]

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
        result_df['lower'] = [np.percentile(value_df[col].values, 2.5) for col in identifiers]
        result_df['upper'] = [np.percentile(value_df[col].values, 97.5) for col in identifiers]
        result_df = result_df.reset_index(drop=True)

        return result_df

    def append_population(self, table: pd.DataFrame):
        """ Appends a new column with population data based on a rows location,
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
