from scipy import signal
from numpy import ndarray
from profilehooks import profile

class Smooth:
    """This class perform a smooth filter on an N-dimensional array.

    Notes:
        Details on the `mode` options:

            'mirror':
                Repeats the values at the edges in reverse order. The value
                closest to the edge is not included.

            'nearest':
                The extension contains the nearest input value.

            'wrap':
                The extension contains the values from the other end of the
                array.

        For example, if the input is [1, 2, 3, 4, 5, 6, 7, 8], and `kernel_size`
        is 7, the following shows the extended data for the various `mode`
        options::

            mode       |   Ext   |         Input          |   Ext
            -----------+---------+------------------------+---------
            'mirror'   | 4  3  2 | 1  2  3  4  5  6  7  8 | 7  6  5
            'nearest'  | 1  1  1 | 1  2  3  4  5  6  7  8 | 8  8  8
            'constant' | 0  0  0 | 1  2  3  4  5  6  7  8 | 0  0  0
            'wrap'     | 6  7  8 | 1  2  3  4  5  6  7  8 | 1  2  3
    """

    def __init__(self, kernel_size: int, polyorder: int, mode='interp'):
        """Create a RollingMedian element.

        extension to use for the padded signal to which the filter is
        applied.

        Args:
            kernel_size (int): The length of the filter window (i.e. the number
                of coefficients).
            polyorder (int): The order of the polynomial used to fit the
                samples.
            mode: Must be 'mirror', 'nearest', 'wrap' or 'interp'. This
                determines the type of
        """
        self.mode = mode
        self.polyorder = polyorder
        self.kernel_size = kernel_size

    @profile
    def process(self, data : ndarray) -> ndarray:
        """Perform a smoothing filter on an N-dimensional array.

        Apply a smoothing filter to the input array using a local window-size
        given by `kernel_size`

        Args:
            data (ndarray): An array containing the data

        Returns:
            An array the same size as input containing the filtered result.
        """
        return signal.savgol_filter(data, window_length=self.kernel_size, polyorder=self.polyorder, mode=self.mode, axis=1)
