import numpy  as np
from nara_wpe.wpe import wpe
from nara_wpe.utils import stft, istft


class DeReverb():
    """ This class implements a de-reverberation technique based on WPE.

    The main algorithm is based on the following paper: Yoshioka, Takuya, and Tomohiro Nakatani.
    “Generalization of multi-channel linear prediction methods for blind MIMO impulse response shortening.”
    IEEE Transactions on Audio, Speech, and Language Processing 20.10 (2012): 2707-2720.

    """

    def __init__(self,
                 fft_size: int = 512,
                 fft_shift: int = 128,
                 iterations: int = 3,
                 delay: int = 3,
                 taps: int = 10):
        """

        Args:
            fft_size (int): Scalar FFT-size.
            fft_shift (int) : Scalar FFT-shift, the step between successive frames in samples. Typically shift is a fraction of size.
            iterations (int): Number of iterations
            delay(int): Delay as a guard interval, such that the input data does not become zero.
            taps (int): Filter order
        """
        self.taps = taps
        self.fft_size = fft_size
        self.fft_shift = fft_shift
        self.iterations = iterations
        self.delay = delay


    def process(self, data: np.ndarray) -> np.ndarray:
        """
        Reduces the reverberant effects in the input signal
        Args:
            data: Multi channel time signal
        Returns:
            Estimated signal with the same shape as data
        """
        y = stft(time_signal=data, size=self.fft_size, shift=self.fft_shift)
        z = wpe(Y=y, iterations=self.iterations, delay=self.delay, taps=self.taps).transpose(1, 2, 0)
        return istft(z, size=self.fft_size, shift=self.fft_shift)