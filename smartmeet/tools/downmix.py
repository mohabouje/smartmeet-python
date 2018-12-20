import numpy as np

class DownMix:
    """Converts a multi-channels data to mono"""
    def process(self, data: np.ndarray) -> np.ndarray:
        """Converts the multi-channel data into a mono signal :param data: N-D
        array representing the multi-channel audio data :param extra: Any
        information previously computed

        Args:
            data (np.ndarray): Multi-Channel array to be down mixed. Expected shape: [Samples per channel, Channels]

        Returns:
            Mono version (average) of the original data.
        """
        return np.mean(a=data, axis=0, dtype=np.float32)