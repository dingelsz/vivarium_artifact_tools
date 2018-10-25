import pandas as pd
import numpy as np

import os.path
from functools import lru_cache, partial
from types import SimpleNamespace

import vivarium_inputs as ceam_inputs
from gbd_mapping import covariates
from vivarium_gbd_access import gbd


class ArtifactTool():

    class _HDF_Path_Parser():
        def __init__(self, level_indicator: str="/", data_name: str="table", hide_path: str=False):
            self.level_indicator = level_indicator
            self.data_name = data_name
            self.hide_path = hide_path
            self.root = {}

        def add(self, path):
            nodes = path.split(self.level_indicator)[1:]
            level = self.root
            while len(nodes) > 0:
                current_node = nodes.pop(0)
                if current_node not in level:
                    level[current_node] = {}
                level = level[current_node]
            level['full_path'] = path

        def to_namespace(self, func):
            return self._dict_to_namespace(self.root, func)

        def _dict_to_namespace(self, level, func):
            for key in level:
                if key != 'full_path':
                    level[key] = self._dict_to_namespace(level[key], func)
            if 'full_path' in level:
                level[self.data_name] = partial(func, level['full_path'])
                if self.hide_path:
                    level.pop('full_path')
            return SimpleNamespace(**level)

    def __init__(self, path):
        assert os.path.isfile(path), (path + " does not exist")
        self._path = path
        self._hdf = pd.HDFStore(path)
        self._str = None
        self._parse_paths()

    def _parse_paths(self):
        """ Parse the paths of the hdf in order to:
            - create a string representing the hdf
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
