from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd
from numpy import dtype, ndarray
from pandas import DataFrame

from Correlations_Distance_matrices_engine.data_loader import DataLoader

class CorrelationDistanceMatrixEngine:
    def __init__(
            self,
            data_loader: DataLoader
    ) -> None:
        self.data_loader : DataLoader = data_loader
        self.raw_series : pd.DataFrame = self.data_loader.load_series_raw()
        self.log_returns_series : pd.DataFrame = self.data_loader.modify_series_log_returns(
            self.raw_series
        )

    def splitter(
            self
    ) -> tuple[DataFrame, DataFrame]:
        mask = self.log_returns_series.index <= datetime(
                2019,
                11,
                25)
        batch_a = self.log_returns_series[mask].dropna()
        batch_b = self.log_returns_series[~mask]

        return batch_a, batch_b

    def yield_correlations(
            self,
            treated_data :pd.DataFrame
    ) -> pd.DataFrame:
        correlation_matrix : pd.DataFrame = pd.DataFrame()
        correlation_matrix = treated_data.corr()
        return correlation_matrix

    def yield_distance_matrix(
            self,
            correlation_matrix: pd.DataFrame
    ) -> ndarray[tuple[int, ...], dtype[Any]]:
        copy = correlation_matrix.copy()
        copy = np.sqrt(2 * (1 - copy))
        return copy

    def make_yields_splitter(
            self,
            splits : tuple[pd.DataFrame, pd.DataFrame]
    ) -> tuple[DataFrame, DataFrame, ndarray[tuple[int, ...], dtype[Any]], ndarray[tuple[int, ...], dtype[Any]]]:
        batch_a_corr = self.yield_correlations(splits[0])
        batch_b_corr = self.yield_correlations(splits[1])
        batch_a_dist = self.yield_distance_matrix(batch_a_corr)
        batch_b_dist = self.yield_distance_matrix(batch_b_corr)

        return batch_a_corr, batch_b_corr, batch_a_dist, batch_b_dist

if __name__ == "__main__":
    engine = CorrelationDistanceMatrixEngine(
        data_loader=DataLoader()
    )
    engine.splitter()