from datetime import timedelta
from typing import List, Any, Tuple, Optional

import matplotlib.colors
import numpy as np
import pandas as pd


class Song:
    def __init__(self, name: str, song: str, profile: str, color: str, release: str, promo: List[Tuple[str, str]] = ()):
        """
        :param name: the song name.
        :param song: the .csv filepath of the song data.
        :param profile: the .csv filepath of the profile data.
        :param color: the color of the song to be used in plots.
        :param release: the release date of the song.
        :param promo: the promo periods, indicated by start and end date.
        """
        release = pd.to_datetime(release)
        # get the song data
        song = pd.read_csv(song)
        song['date'] = pd.to_datetime(song['date'])
        song = song.set_index('date').sort_index()
        # get the profile data
        profile = pd.read_csv(profile).rename(columns={'streams': 'tot streams'})
        profile['date'] = pd.to_datetime(profile['date'])
        profile = profile.set_index('date').sort_index()
        # merge and process the two dataframes
        data = song.join(profile)
        data['followers'] = data['followers'] - data['followers'][release - timedelta(days=1)]
        # store results
        self.data: pd.DataFrame = data
        self.name: str = name
        self.color: str = color
        self.release: Any = release
        self.promos: List[Tuple[Any, Any]] = [(pd.to_datetime(s), pd.to_datetime(e)) for s, e in promo]

    def rolling(self, window: int = 1, win_type: Optional[str] = 'exponential') -> pd.DataFrame:
        """Creates a processed dataframe by averaging over a rolling window.

        :param window: the moving average window size.
        :param win_type: the moving average window type.
        :return: a single processed dataframe.
        """
        data = self.data.rolling(window=window, win_type=win_type, center=True).mean().dropna()
        data = data[data.index >= self.release - timedelta(days=1)]
        return data.reset_index().reset_index(names='day')


def merge_songs(songs: List[Song], window: int = 1, win_type: Optional[str] = 'exponential') -> pd.DataFrame:
    """Creates a single processed dataframe from multiple songs.

    :param songs: the list of songs to process.
    :param window: the moving average window size.
    :param win_type: the moving average window type.
    :return: a single processed dataframe.
    """
    data = [song.rolling(window=window, win_type=win_type) for song in songs]
    data = pd.concat(data, keys=[song.name for song in songs], names=['Song']).reset_index()
    return data.drop(columns='level_1')


def blend_color(c1: str, c2: str = '#FFFFFF', alpha: float = 0.5) -> str:
    """Interpolates two colors given the factor alpha. When the second factor is white (#FFFFFF) it simulates alpha
    transparency on white background (this is useful for .eps plots which do not support transparency, and also to have
    a fake transparent color without showing the background grid).
    
    :param c1: the first color.
    :param c2: the second color.
    :param alpha: the interpolation factor in [0, 1].
    :return: the blended color.
    """
    c1 = np.array(matplotlib.colors.ColorConverter.to_rgb(c1))
    c2 = np.array(matplotlib.colors.ColorConverter.to_rgb(c2))
    c = alpha * c1 + (1 - alpha) * c2
    r, g, b = np.array(255 * c, dtype=int)
    return f"#{r:02x}{g:02x}{b:02x}".upper()
