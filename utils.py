from typing import List, Any, Optional

import numpy as np
import pandas as pd


class Song:
    def __init__(self, name: str, path: str, color: str, release: str):
        """
        :param name: the song name.
        :param path: the .csv filepath of the song.
        :param color: the color of the song to be used in plots.
        :param release: the release date of the song.
        """
        data = pd.read_csv(path)
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date').sort_index()
        self.data: pd.DataFrame = data
        self.name: str = name
        self.path: str = path
        self.color: str = color
        self.release: Any = pd.to_datetime(release)


def process(songs: List[Song], window: int = 0, win_type: str = 'exponential') -> pd.DataFrame:
    """
    :param songs: the list of songs to process.
    :param window: the moving average window size.
    :param win_type: the moving average window type.
    :return: a single processed dataframe.
    """

    def _process(df: pd.DataFrame, release: Optional) -> pd.DataFrame:
        df = df.copy()
        if window > 0:
            df = df.rolling(window, win_type=win_type).mean().dropna()
        if release is not None:
            df = df[df.index >= release]
        df = df.reset_index()
        df['day'] = np.arange(len(df)) + 1
        df['cumulative streams'] = df['streams'].cumsum()
        return df

    data = [_process(df=s.data, release=s.release) for s in songs]
    return pd.concat(data, keys=[s.name for s in songs], names=['Song'])
