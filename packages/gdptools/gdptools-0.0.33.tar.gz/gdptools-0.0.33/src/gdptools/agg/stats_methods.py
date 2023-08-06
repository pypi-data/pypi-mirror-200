"""Statistical Funtions for aggregation."""
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt


@dataclass  # type: ignore[misc]
class StatsMethod(ABC):
    """Abstract method for gdptools weighted stats."""

    array: npt.NDArray  # type: ignore
    weights: npt.NDArray[np.double]
    def_val: Any

    @abstractmethod
    def get_stat(
        self,
    ) -> Any:
        """Abstract method for aquiring stats."""
        pass


@dataclass
class MAWeightedMean(StatsMethod):
    """Weighted Masked Mean."""

    def get_stat(self) -> Any:
        """Get weighted masked mean."""
        masked = np.ma.masked_array(self.array, np.isnan(self.array))
        try:
            tmp = np.ma.average(masked, weights=self.weights, axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return tmp


@dataclass
class WeightedMean(StatsMethod):
    """Weighted Mean."""

    def get_stat(self) -> Any:
        """Get weighted mean."""
        try:
            tmp = np.average(self.array, weights=self.weights, axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return tmp


@dataclass
class WeightedStd(StatsMethod):
    """Weighted Standard Deviation."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> Any:
        """Get weighted standard deviation."""
        avg = np.average(self.array, weights=self.weights, axis=1)
        # variance = np.average((self.array - avg)**2, weights=self.weights, axis=1)
        variance = np.average(
            np.subtract(self.array, avg[:, None]) ** 2, weights=self.weights, axis=1
        )
        return np.sqrt(variance)


@dataclass
class MAWeightedStd(StatsMethod):
    """Weighted Masked Standard Deviation."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> Any:
        """Get weighted masked standard deviation."""
        masked = np.ma.masked_array(self.array, np.isnan(self.array))
        avg = np.ma.average(self.array, weights=self.weights, axis=1)
        # avg = np.average(masked, weights=self.weights, axis=1)
        # avg = np.average(masked, weights=self.weights)
        # variance = np.average((masked - avg)**2, weights=self.weights, axis=1)
        variance = np.ma.average(
            np.subtract(masked, avg[:, None]) ** 2, weights=self.weights, axis=1
        )
        return np.sqrt(variance)


@dataclass
class MAWeightedMedian(StatsMethod):
    """Weighted Masked Median."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def _get_median(self, array: npt.NDArray, weights: npt.NDArray[np.double]) -> Any:
        """_get_median Get median values.

        _extended_summary_

        Args:
            array (npt.NDArray): _description_
            weights (npt.NDArray[np.double]): _description_

        Returns:
            Any: _description_
        """
        quantile = 0.5
        # zip and sort array values and their corresponding weights
        pairs = sorted(list(zip(array, weights)))  # noqa
        i, prev_wght, next_wght, wght_sum, next_val = 0, 0, 0, 0, 0
        while wght_sum <= quantile:
            prev_val, prev_wght = next_val, next_wght
            next_val, next_wght = pairs[i]
            wght_sum += next_wght
            i += 1
        return (prev_wght * prev_val + next_wght * next_val) / (prev_wght + next_wght)

    def get_stat(self) -> Any:
        """Get weighted masked median."""
        masked = np.ma.masked_array(self.array, np.isnan(self.array))
        maweights = np.ma.masked_array(self.weights, np.isnan(self.weights))
        return np.apply_along_axis(self._get_median, 1, masked, maweights)


@dataclass
class WeightedMedian(StatsMethod):
    """Weighted Median."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def _get_median(self, array: npt.NDArray, weights: npt.NDArray[np.double]) -> Any:
        """_get_median Get median values.

        _extended_summary_

        Args:
            array (npt.NDArray): _description_
            weights (npt.NDArray[np.double]): _description_

        Returns:
            Any: _description_
        """
        # First check to see if there are NoData values. Function will return np.nan
        # if there are NoData values, as medians cannot be calculated if NoData values
        # exist.
        if np.isnan(array).any():
            return np.nan

        quantile = 0.5
        # zip and sort array values and their corresponding weights
        pairs = sorted(list(zip(array, weights)))  # noqa
        i, prev_wght, next_wght, wght_sum, next_val = 0, 0, 0, 0, 0
        while wght_sum <= quantile:
            prev_val, prev_wght = next_val, next_wght
            next_val, next_wght = pairs[i]
            wght_sum += next_wght
            i += 1
        return (prev_wght * prev_val + next_wght * next_val) / (prev_wght + next_wght)

    def get_stat(self) -> Any:
        """Get weighted median."""
        return np.apply_along_axis(self._get_median, 1, self.array, self.weights)


@dataclass
class MACount(StatsMethod):
    """Masked Count."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> Any:
        """Get count of masked grid cells."""
        masked = np.ma.masked_array(self.array, np.isnan(self.array))
        weight_mask = self.weights == 0
        return np.ma.masked_array(masked, mask=weight_mask | masked.mask).count(axis=1)


@dataclass
class Count(StatsMethod):
    """Count."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> Any:
        """Get count of grid cells."""
        return np.ma.masked_array(self.weights, mask=self.weights == 0).count()


@dataclass
class MAMin(StatsMethod):
    """Masked Minimum Value."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> Any:
        """Get masked min."""
        masked = np.ma.masked_array(self.array, np.isnan(self.array))
        return np.ma.min(masked, axis=1)


@dataclass
class Min(StatsMethod):
    """Minimum Value."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> Any:
        """Get min value."""
        return np.min(self.array, axis=1)


@dataclass
class MAMax(StatsMethod):
    """Masked Maximum Value."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> Any:
        """Get masked max value."""
        masked = np.ma.masked_array(self.array, np.isnan(self.array))
        return np.ma.max(masked, axis=1)


@dataclass
class Max(StatsMethod):
    """Maximum Value."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> Any:
        """Get max value."""
        return np.max(self.array, axis=1)
