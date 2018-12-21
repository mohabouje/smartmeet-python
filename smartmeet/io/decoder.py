from soundfile import SoundFile

class Decoder:
    """This class is an interface to read data from an audio file"""

    def __init__(self, file: str):
        """Creates an instance of a Decoder source with the given configuration

        Args:
            file_name (str): Input file name
            frames_per_buffer (int): Number of frames per buffer.
            name (str): Name of the element
        """
        self.__instance = SoundFile(file=file, mode='r')

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

    @property
    def frames(self) -> int:
        """ Number of available frames"""
        return self.__instance.frames

    def done(self) -> bool:
        """Checks if there still data to read from the audio file"""
        return self.__instance.tell() < self.__instance.frames

    def start(self):
        """Starts the streaming"""
        self.__instance.seek(0)

    def stop(self):
        """Stops the streaming by seeking the file to the end"""
        self.__instance.seek(self.__instance.frames)

    def timestamp(self):
        """Returns the current streaming timestamp in seconds"""
        return self.__instance.tell() / self.__instance.samplerate

    def seek(self, frames: int):
        """Set the read position.

        Args:
            frames (int): The frame index or offset to seek

        Returns:
            The new absolute read/write position in frames
        """
        return self.__instance.seek(frames=frames)

    def read(self, frames_per_channel: int = -1):
        """Returns the buffer read from the audio file"""

        if frames_per_channel is -1:
            frames_per_channel = self.__instance.frames

        return self.__instance.read(frames=frames_per_channel, dtype='float32', always_2d=False)
