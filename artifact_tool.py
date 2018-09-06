import pandas as pd
import numpy as np

import os.path
from functools import lru_cache, partial
from types import SimpleNamespace

import ceam_inputs
from gbd_mapping import covariates
from vivarium_gbd_access import gbd


class ArtifactTool():

    class _HDF_Path_Parser():
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
            level['table'] = path

        def to_namespace(self, func):
            return self._dict_to_namespace(self.root, func)

        def _dict_to_namespace(self, root, func):
            for key in root:
                if key == 'table':
                    continue
                root[key] = self._dict_to_namespace(root[key], func)
            if 'table' in root:
                root['table'] = partial(func, root['table'])
            return SimpleNamespace(**root)

    def __init__(self, path):
        assert os.path.isfile(path), (path + " does not exist")
        self._path = path
        self._hdf = pd.HDFStore(path)
        self._str = None
        self._parse_paths()
        self.covariates = self._create_covariates()
        self.locations = self._create_locations()

    def _parse_paths(self):
        """ Parse the paths of the hdf in order to:
            - create a string representing the hdf
            - collect each cause and risk
            - store path information in the AT
        """
        self._str = "HDF: " + self._path + "\n"
        self._str += "---Table Map---\n"

        self._table_paths = []

        path_parser = self._HDF_Path_Parser()

        for path, _ in self._hdf.items():
            path_parser.add(path)
            self._table_paths.append(path)

            path_list = path.split('/')
            path_list = path_list[1:]

            self._str += str(path) + "\n"

        self.tables = path_parser.to_namespace(self._get_table)

    def _create_covariates(self):
        covars = covariates.to_dict()
        covars = {c: partial(gbd.get_covariate_estimates, [covars[c]['gbd_id']]) for c in covars}

        return SimpleNamespace(**covars)

    def _create_locations(self):
        location_table = gbd.get_location_ids()
        location_map = dict(list(zip(location_table.location_name, location_table.location_id)))
        return SimpleNamespace(**location_map)

    def _get_table(self, path):
        return self._hdf.get(path)

    def __str__(self):
        return self._str

    def __del__(self):
        self._hdf.close()

    @lru_cache(maxsize=16)
    def population_for_year_with_age_limit(self, year: int=2016, lower: float=0, upper: float=5):
        table = self._hdf.get('/population/structure')
        table = table[table.year == year]
        table = table[table.age <= upper]
        table = table[table.age >= lower]
        return table.population.sum() / 2

    @lru_cache(maxsize=16)
    def population_for_year(self, year: int=2016):
        return self.population_for_year_with_age_limit(year, 0, 1000)
