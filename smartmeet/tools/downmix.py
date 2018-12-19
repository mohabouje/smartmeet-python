import numpy as np
from smartmeet.core.filter import Filter


class DownMix(Filter):
    """ Converts a multi-channels data to mono
    """
    def process(self, data, extra) -> tuple:
        """ Converts the multi-channel data into a mono signal
        Args:
            data: N-D array representing the multi-channel audio data
            extra: Any information previously computed

        Returns:
            Mono version (average) of the original data.
        """
        return np.mean(a=data, axis=0, dtype=np.float32), extra