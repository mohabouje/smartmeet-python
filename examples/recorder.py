from argparse import ArgumentParser
from smartmeet.core.pipeline import Pipeline
from smartmeet.io.recorder import Recorder
from smartmeet.io.encoder import Encoder
from smartmeet.filter.pre_emphasis import PreEmphasis


def main():
    parser = ArgumentParser(description='Records data from the input microphone and save it into an audio file.')
    parser.add_argument('-f', '--file', required=True, dest='file', type=str, help='File name of the output file')
    parser.add_argument('-c', '--channels', required=True, dest='channels', type=int, help='Number of channels')
    parser.add_argument('-s', '--sample-rate', required=True, dest='rate', type=int, help='Sampling rate in Hz')
    parser.add_argument('-d', '--device', dest='device', type=str, default="default", help="Name of the input interface")
    args = parser.parse_args()

    recorder = Recorder(rate=args.rate, channels=args.channels, device_name=args.device,
                        frames_per_buffer=args.rate / 100)
    encoder = Encoder(file_name=args.file, rate=args.rate, channels=args.channels)
    emphasis = PreEmphasis()


    recorder.link(emphasis)
    emphasis.link(encoder)

    pipeline = Pipeline()
    return pipeline.start(recorder)



if __name__ == '__main__':
    main()