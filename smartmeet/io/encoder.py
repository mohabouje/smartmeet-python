from soundfile import SoundFile

from smartmeet.core.sink import Sink


class Encoder(Sink):
    """This class is an interface to write data into an audio file"""

    def __init__(self, file_name: str, rate: int, channels: int, name: str = ""):
        """Creates an instance of a Encoder source with the given configuration

        Args:
            file_name (str): Input file name
            rate (int): The sample rate of the file in Hz
            channels (int): The number of channels
            name (str): Name of the element
        """
        super().__init__(name)
        self.__instance = SoundFile(file=file_name, mode='w', samplerate=rate, channels=channels)

    @property
    def sample_rate(self) -> int:
        """Return the sampling rate in Hz."""
        return self.__instance.samplerate

    @property
    def channels(self) -> int:
        """Return the number of channels."""
        return self.__instance.channels

    @property
    def file_name(self) -> str:
        """Return the file name."""
        return self.__instance.name

    def seek(self, frames):
        """Set the write position.

        Args:
            frames: The frame index or offset to seek
        """
        return self.__instance.seek(frames=frames)

    def process(self, data, extra=None):
        """Writes the buffer of data into the audio file.

        Args:
            data: Array to write in the file
            extra: Any extra information previously computed.
        """
        self.__instance.write(data.flatten()), extra
