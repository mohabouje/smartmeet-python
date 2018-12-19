from speechpy.processing import preemphasis

from smartmeet.core.filter import Filter


class PreEmphasis(Filter):
    """
    This class perform a pre-emphasis filter on an N-dimensional array.
    """

    def __init__(self, cof: float = 0.95, name: str = ""):
        """ Create a MedianFilter element.

        :param cof: The pre-emphasising coefficient. 0 equals to no filtering.
        :param name: Element's name also known as alias
        """
        super().__init__(name)
        self.cof = cof

    def process(self, data, extra=None):
        """ Perform a pre-emphasis filter on an N-dimensional array.

        Apply a pre-emphasis filter to the input array using a local window-size given by `kernel_size`

        :param data: An array containing the data
        :param extra: Dictionary storing any extra information previously computed.
        :return: An array the same size as input containing the filtered data and the dictionary.
        """
        return preemphasis(signal=data, cof=self.cof), extra
