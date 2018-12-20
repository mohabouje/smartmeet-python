from speechpy.processing import preemphasis
from numpy import ndarray
from profilehooks import profile

class PreEmphasis:
    """This class perform a pre-emphasis filter on an N-dimensional array."""

    def __init__(self, cof: float = 0.95):
        """Create a MedianFilter element.

        Args:
            cof (float): The pre-emphasising coefficient. 0 equals to no
                filtering.
        """
        self.cof = cof

    @profile
    def process(self, data : ndarray) -> ndarray:
        """Perform a pre-emphasis filter on an N-dimensional array.

        Apply a pre-emphasis filter to the input array using a local
        window-size given by `kernel_size`

        Args:
            data (ndarray): An array containing the data

        Returns:
            An array the same size as input containing the filtered data and the
            dictionary.
        """
        # TODO: replace this with an implementation with numpy
        return preemphasis(signal=data, cof=self.cof)
