"""Load data for morphing."""

from importlib.resources import files
from itertools import zip_longest
from numbers import Number
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes

from .. import MAIN_DIR
from ..plotting.style import plot_with_custom_style
from .dataset import Dataset


class DataLoader:
    """
    Class for loading datasets for morphing.

    .. plot::
       :caption:
            Datasets currently included in ``data_morph``. Note that CSV
            files are also supported by :meth:`.load_dataset`.

        from data_morph.data.loader import DataLoader
        DataLoader.plot_available_datasets()
    """

    _DATA_PATH: str = 'data/starter_shapes/'
    _DATASETS: dict = {
        'cat': 'cat.csv',
        'dino': 'dino.csv',
        'dog': 'dog.csv',
        'music': 'music.csv',
        'panda': 'panda.csv',
        'sheep': 'sheep.csv',
    }
    AVAILABLE_DATASETS = sorted(list(_DATASETS.keys()))
    """list[str]: List of available built-in starter datasets,
    which can be visualized with :meth:`plot_available_datasets`."""

    def __init__(self) -> None:
        raise NotImplementedError

    @classmethod
    def load_dataset(
        cls,
        dataset: str,
        scale: Number = None,
    ) -> Dataset:
        """
        Load dataset.

        Parameters
        ----------
        dataset : str
            Either one of :attr:`AVAILABLE_DATASETS` or a path to a
            CSV file containing two columns: x and y.
        scale : numbers.Number, optional
            The factor to scale the data by (can be used to speed up morphing).
            Values in the data's x and y columns will be divided by this value.

        Returns
        -------
        Dataset
            The starting dataset for morphing.

        Notes
        -----
        If you are looking to create a :class:`.Dataset` from a
        :class:`~pandas.DataFrame` object, use the :class:`.Dataset`
        class directly.
        """
        try:
            filepath = files(MAIN_DIR).joinpath(
                Path(cls._DATA_PATH) / cls._DATASETS[dataset]
            )
            name = dataset
            df = pd.read_csv(filepath)
        except KeyError:
            try:
                name = Path(dataset).stem
                df = pd.read_csv(dataset)
            except FileNotFoundError:
                raise ValueError(
                    f'Unknown dataset "{dataset}". '
                    'Provide a valid path to a CSV dataset or use one of '
                    f'the included datasets: {", ".join(cls.AVAILABLE_DATASETS)}.'
                )
        return Dataset(name=name, df=df, scale=scale)

    @classmethod
    @plot_with_custom_style
    def plot_available_datasets(cls) -> Axes:
        """
        Plot the built-in datasets.

        Returns
        -------
        matplotlib.axes.Axes
            The :class:`~matplotlib.axes.Axes` object containing the plot.

        See Also
        --------
        AVAILABLE_DATASETS
            The list of available datasets built into ``data_morph``.
        """
        num_plots = len(cls.AVAILABLE_DATASETS)
        num_cols = 3
        num_rows = int(np.ceil(num_plots / num_cols))

        fig, axs = plt.subplots(
            num_rows,
            num_cols,
            layout='constrained',
            figsize=(12, 4 * num_rows),
            subplot_kw={'aspect': 'equal'},
        )
        fig.get_layout_engine().set(w_pad=0.2, h_pad=0.2)

        for dataset, ax in zip_longest(cls.AVAILABLE_DATASETS, axs.flatten()):
            if dataset:
                ax.tick_params(
                    axis='both',
                    which='both',
                    bottom=False,
                    left=False,
                    right=False,
                    labelbottom=False,
                    labelleft=False,
                )
                points = cls.load_dataset(dataset)
                points.df.plot(
                    x='x',
                    y='y',
                    color='k',
                    kind='scatter',
                    title=f'{dataset} ({points.df.shape[0]:,d} points)',
                    ax=ax,
                    xlim=points.plot_bounds.x_bounds,
                    ylim=points.plot_bounds.y_bounds,
                )
                ax.set(xlabel='', ylabel='')
            else:
                ax.remove()
        return axs
