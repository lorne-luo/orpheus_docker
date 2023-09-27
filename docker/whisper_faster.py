import click as click
from faster_whisper import WhisperModel


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--language', '-l', default='zh', required=False, help='Language')
@click.option('--model', '-m', default='large-v2', required=False, help='Model file or data')
def main(input, language, model):
    if model == 'large':
        model = 'large-v2'
    # Run on GPU with FP16
    # model = WhisperModel(model, device="cuda", compute_type="float16")

    # or run on GPU with INT8
    # model = WhisperModel(model, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    model = WhisperModel(model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(input, language=language, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))


if __name__ == '__main__':
    main()
