"""Convenient plotting wrapper around matplotlib."""

__version__ = "1.0.0"

from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

Y = Any
X = Any
Z = Any
XY = Tuple[X, Y]
XYZ = Tuple[X, Y, Z]
NativeArgument = Any
CycledArguments = Optional[Union[NativeArgument, List[Optional[NativeArgument]], Tuple[Optional[NativeArgument]]]]
ClippedArguments = Optional[Union[NativeArgument, List[Optional[NativeArgument]], Tuple[Optional[NativeArgument]]]]


class ChartError(ValueError):
	pass


def _cycle(arguments: CycledArguments, index: int) -> Optional[NativeArgument]:
	if arguments is not None:
		if isinstance(arguments, (list, tuple)):
			return arguments[index % len(arguments)]
		else:
			return arguments


def _clip(arguments: CycledArguments, index: int) -> Optional[NativeArgument]:
	if arguments is not None:
		if isinstance(arguments, (list, tuple)):
			try:
				return arguments[index]
			except IndexError:
				pass
		else:
			return arguments


def _cycle_and_set(dictionary, key, arguments: CycledArguments, index: int) -> None:
	value = _cycle(arguments, index)
	if value is not None:
		dictionary[key] = value
	elif key in dictionary:
		del dictionary[key]


def _clip_and_set(dictionary, key, arguments: CycledArguments, index: int) -> None:
	value = _clip(arguments, index)
	if value is not None:
		dictionary[key] = value
	elif key in dictionary:
		del dictionary[key]


def plot(*datasets: Union[XY, Y, XYZ], kind='plot', flatten: bool = True, transpose: Optional[bool] = None, xcolumn: Optional[str] = 'x', guess_label: bool = True, label: ClippedArguments = None, color: CycledArguments = None, marker: ClippedArguments = None, linestyle: ClippedArguments = None, linewidth: ClippedArguments = None, markersize: ClippedArguments = None, legend: Optional[bool] = None, title: Optional[str] = None, xlabel: Optional[str] = None, ylabel: Optional[str] = None,
         figsize: Tuple[float, float] = (10, 8), dpi: float = 100, subplots_parameters: Optional[Dict[str, Any]] = None, show: bool = True, grid: Optional[bool] = False, grid_which: str = 'major', grid_axis: str = 'both', grid_kwargs: Optional[Dict[str, Any]] = None, theme='seaborn-v0_8-deep', **plotter_parameters) -> Tuple[plt.Figure, plt.Axes, List[plt.Artist]]:  # figsize: Tuple[float,
	# float] = plt.rcParams["figure.figsize"]
	if subplots_parameters is None:
		subplots_parameters = {}
	plt.style.use(theme)
	fig, ax = plt.subplots(figsize=figsize, dpi=dpi, **subplots_parameters)
	try:
		plotter = getattr(ax, kind)
	except AttributeError:
		raise ChartError(f'Plot kind {kind} cold not be found.')
	normalized_datasets = []
	if xcolumn is not None:
		for dataset in datasets:
			if isinstance(dataset, pd.DataFrame) and len(dataset.columns) > 1 and xcolumn in dataset.columns:
				for column in dataset.columns:
					if column != xcolumn:
						normalized_datasets.append(dataset[[xcolumn, column]])
			else:
				normalized_datasets.append(dataset)
	else:
		normalized_datasets = datasets
	diagrams = []
	x_minimum = x_maximum = y_minimum = y_maximum = 0
	labels_count = 0
	for i, dataset in enumerate(normalized_datasets):
		params = plotter_parameters.copy()
		for k, v in plotter_parameters.items():
			_clip_and_set(params, k, v, i)
		_clip_and_set(params, 'label', label, i)
		_cycle_and_set(params, 'color', color, i)
		_clip_and_set(params, 'marker', marker, i)
		_clip_and_set(params, 'linestyle', linestyle, i)
		_clip_and_set(params, 'linewidth', linewidth, i)
		_clip_and_set(params, 'markersize', markersize, i)
		vectors = np.asarray(dataset)
		if transpose is True or transpose is None and isinstance(dataset, pd.DataFrame):
			vectors = vectors.T
		if guess_label and 'label' not in params and isinstance(dataset, pd.DataFrame):
			label_guess = str(dataset.columns[-1])
			if label_guess:
				params['label'] = label_guess
		if len(vectors.shape) > 1 and flatten:
			vectors = np.array([vector.flatten() for vector in vectors])
		elif len(vectors.shape) == 1:
			vectors = vectors.reshape((1, vectors.shape[0]))
		if 'label' in params:
			labels_count += 1
		diagrams.append(plotter(*vectors, **params))
		if vectors.shape[0] == 1:
			x_minimum = min(x_minimum, 0)
			x_maximum = max(x_maximum, vectors.shape[1] - 1)
			y_minimum = min(y_minimum, vectors.min())
			y_maximum = max(y_maximum, vectors.max())
		else:
			minimums = vectors.min(axis=1)
			maximums = vectors.max(axis=1)
			x_minimum = min(x_minimum, minimums[0])
			x_maximum = max(x_maximum, maximums[0])
			y_minimum = min(y_minimum, minimums[1:].min())
			y_maximum = max(y_maximum, maximums[1:].max())
	diagrams = [diagram for container in diagrams for diagram in container]
	if legend is True or legend is None and len(diagrams) > 1 and labels_count:
		ax.legend()
	if xlabel is not None:
		ax.set_xlabel(xlabel)
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	if title is not None:
		ax.set_title(title)
	ax.set_xlim((x_minimum, x_maximum))
	ax.set_ylim((y_minimum, y_maximum))
	if grid in [True, None]:
		plt.grid(visible=grid, which=grid_which, axis=grid_axis, **(grid_kwargs or {}))
	if show:
		plt.show()
	return fig, ax, diagrams
