import time
from queue import Queue
import numpy
from pyaudio import PyAudio, paContinue, paFloat32
from smartmeet.core.source import Source


class Recorder(Source):
    """
    This class is an interface to pyAudio that performs the retrieval of recorded audio buffers
    from an input device.
    """
    def __init__(self, rate: int = 16000, frames_per_buffer: int = None,
                 channels: int = 1, device_name: str = "default", name: str = ""):
        """ Creates an instance of a Recorder source with the given configuration

        :param rate: Sampling rate in Hz
        :param channels: Number of channels
        :param device_name: Input device name
        :param frames_per_buffer: Number of frames per buffer.
        """
        super().__init__(name)
        self.__queue = Queue()
        self.__rate = rate
        self.__frames_per_buffer = int(frames_per_buffer if frames_per_buffer else rate // 100)
        self.__channels = channels
        self.__instance = PyAudio()

        for i in range(self.__instance.get_device_count()):
            dev = self.__instance.get_device_info_by_index(i)
            name = dev['name'].encode('utf-8')
            if name.find(device_name.encode('utf-8')) >= 0:
                self.__device_index = i
                break
        else:
            self.__device_index = self.__instance.get_default_input_device_info()['index']

        if self.__device_index is None:
            raise ValueError('Can not find the input device {}'.format(device_name))

        self.__stream = self.__instance.open(
            start=False,
            format=paFloat32,
            input_device_index=self.__device_index,
            channels=self.__channels,
            rate=int(self.__rate),
            frames_per_buffer=int(self.__frames_per_buffer),
            stream_callback=self.__audio_callback,
            input=True
        )

    def __decode(self, data):
        """
        Convert a byte stream into a 2D numpy array with
        shape (chunk_size, channels)

        Samples are interleaved, so for a stereo stream with left channel
        of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output
        is ordered as [L0, R0, L1, R1, ...]
        """
        result = numpy.fromstring(string=data, dtype=numpy.float32)
        return numpy.reshape(result, (self.frames_per_buffer, self.channels))


    def __audio_callback(self, in_data, frame_count, time_info, status):
        self.__queue.put(self.__decode(data=in_data))
        return None, paContinue

    @property
    def sample_rate(self) -> int:
        """ Return the sampling rate in Hz. """
        return self.__rate

    @property
    def channels(self):
        """ Return the number of channels. """
        return self.__channels

    @property
    def device_name(self):
        """ Return the device name. """
        return self.__instance.get_device_info_by_index(self.__device_index)["name"]

    @property
    def frames_per_buffer(self) -> int:
        """ Returns the number of frames per channel"""
        return self.__frames_per_buffer

    def ready(self):
        return not self.__queue.empty()

    def done(self):
        """ Checks if the stream is currently active """
        return self.__stream.is_stopped()

    def process(self):
        """ Returns the oldest recorded buffer
        :return: Array containing the samples read from a file
        """
        while (self.__queue.empty()):
            time.sleep(self.frames_per_buffer / self.sample_rate)

        return self.__queue.get(), dict()

    def start(self):
        """ Starts the audio streaming """
        self.__stream.start_stream()

    def stop(self):
        """ Stops the audio streaming """
        self.__stream.stop_stream()
