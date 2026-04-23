
from pathlib import Path
import pandas as pd
import numpy as np

class DataLoader:
    def __init__(
            self
    )->None:
        self.data_path = Path(__file__).resolve().parent.parent / "data"

    def load_dir(
            self
    )-> list[str]:
        data_sources : list[str] = []
        for path in self.data_path.glob("*.csv"):
            data_sources.append(path.name)

        return data_sources

    def load_data(
            self,
            name
    )->pd.DataFrame:
        data = pd.read_csv(self.data_path / name, index_col=1)
        data.drop(columns=["Unnamed: 0"], inplace=True)
        data.index = pd.to_datetime(data.index)
        return data

    def load_series_raw(
            self,
    ) -> pd.DataFrame:
        sources : list[str] = self.load_dir()
        sources_col : list[str] = [item.removesuffix("_data.csv") for item in sources]
        raw_table = pd.DataFrame()
        for source in sources:
            if raw_table is None:
                raw_table = self.load_data(source)
            else:
                raw_table[source] = self.load_data(source)

        raw_table.columns = sources_col
        return raw_table

    def modify_series_log_returns(
            self,
            raw_series : pd.DataFrame
    ) -> pd.DataFrame:
        treated_data = pd.DataFrame(index=raw_series.index)
        for source in raw_series.columns:
            treated_data[source] = np.log(raw_series[source] / raw_series[source].shift(1)).dropna()

        return treated_data