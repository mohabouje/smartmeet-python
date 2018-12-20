import numpy as np


class Converter:

    @staticmethod
    def interleave(data: np.ndarray):
        return data.flatten()

    @staticmethod
    def deinterleave(data, frames_per_buffer: int, channels: int, dtype) -> np.ndarray:
        """Convert a byte stream into a 2D numpy array with shape (chunk_size,
        channels)

        Samples are interleaved, so for a stereo stream with left channel of
        [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output is
        ordered as [L0, R0, L1, R1, ...]

        Args:
            data:
            frames_per_buffer:
            channels:
            dtype:
        """
        result = np.fromstring(string=data, dtype=dtype)
        return np.reshape(result, (frames_per_buffer, channels))

    @staticmethod
    def fromFloat16ToS16(data: np.ndarray) -> np.ndarray:
        data[data > np.info(np.int16).max] = np.info(np.int16).max
        data[data < np.info(np.int16).min] = np.info(np.int16).min
        return data.astype(dtype=np.int16)

    @staticmethod
    def fromS16ToFloat16(data: np.ndarray) -> np.ndarray:
        return data.astype(dtype=np.float32)
