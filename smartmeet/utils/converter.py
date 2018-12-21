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
    def fromFloatToInt16(data: np.ndarray) -> np.ndarray:
        temp = data.copy()
        temp[temp > 1.0] = 1.0
        temp[temp < -1.0] = -1.0
        temp[temp < 0] *= abs(np.iinfo(np.int16).min)
        temp[temp > 0] *= abs(np.iinfo(np.int16).max)
        return temp.astype(dtype=np.int16)

    @staticmethod
    def fromInt16ToFloat(data: np.ndarray) -> np.ndarray:
        temp = data.astype(dtype=np.float32)
        temp[temp < 0] /= float(abs(np.iinfo(np.int16).min))
        temp[temp > 0] /= float(abs(np.iinfo(np.int16).max))
        return temp
