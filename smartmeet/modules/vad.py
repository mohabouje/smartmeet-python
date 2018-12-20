import numpy as np
from smartmeet.utils.converter import Converter
from profilehooks import profile
from webrtcvad import Vad

class VAD:
    """This class implements a Voice Activity Detector.

    The voice activity detector is a critical component in any speech
    processing application. It is able to identify the presence or absence of
    human speech in an audio frame.

    Generally, It is used to deactivate some processes during non-speech
    section of an audio session, saving on computation and on network bandwidth.

    Notes:
        This algorithm was implemented in the WebRTC project. The algorithm was
        originally designed to work with 8KHz, 16 bit PCM, mono audio samples.

        The algorithm accepts sampling rates of 8000Hz, 16000Hz, 32000Hz and
        48000Hz, but internally all processing will be done 8000 Hz, input data
        in higher sample rates will just be down-sampled first.
    """

    def __init__(self, rate: int = 8000, mode: int = 0):
        """Creates a VAD detector with the given configuration

        Args:
            rate (int): The audio sample rate, in Hz.
            mode (int): Operational mode,
        must be [0, 3]
        """
        self.__rate = rate
        self.__mode = mode
        self.__vad = Vad(mode=mode)

    @property
    def mode(self) -> int:
        """Returns an integer representing the operational mode"""
        return self.__mode

    @property
    def sample_rate(self) -> int:
        """Returns the sampling rate in Hz."""
        return self.__rate

    @mode.setter
    def mode(self, mode: int):
        """Set the operational mode of the VAD

        A more aggressive (higher mode) VAD is more restrictive in reporting
        speech.

        Put in other words the probability of being speech when the VAD
        returns 1 is increased with increasing mode. As a consequence also the
        missed detection rate goes up.

        Valid modes are:
            - 0 ("quality"):
            - 1 ("low bitrate"),
            - 2 ("aggressive")
            - 3 ("very aggressive").

        The default mode is 0.

        Args:
            mode (int): Operational moder, must be [0, 3]
        """
        self.__mode = mode
        self.__vad.set_mode(mode)

    @profile
    def process(self, data: np.ndarray) -> bool:
        """Checks if the given data contains human speech.

        Args:
            data (np.ndarray): An array containing the data

        Returns:
            True if the audio data contains speech, false otherwise

        Notes:
            The input data must be an array of signed 16-bit samples or an array
            of floating points storing values in the same range [-32,768,
            32,768]

            Only mono frames with a length of 10, 20 or 30 ms are supported. For
            instance, if the class is using a sampling rate of 8KHz, the
            processing function is expecting an numpy.ndarray of shape [80, N],
            [160, N] or [240, N] where N is the number of channels in the input
            data. The signal may be down-mixed to a single channel before
            processing.
        """
        mono = np.mean(a=data, axis=0, dtype=np.float32)
        mono = Converter.fromFloat16ToS16(mono)
        mono = Converter.interleave(mono)
        result = self.__vad.is_speech(buf=mono, sample_rate=self.sample_rate, length=mono.size())
        if (result < 0):
            raise RuntimeError("Invalid frame length. Only frames with a length of 10, 20 or 30 ms are supported.")
        return result
