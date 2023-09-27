import click
from datetime import *
from whisper_jax import FlaxWhisperPipline


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--language', '-l', default='zh', required=False, help='Language')
@click.option('--model', '-m', default='medium', required=False, help='Model file or data')
def main(input, language, model):
    start=datetime.now()
    # instantiate pipeline
    pipeline = FlaxWhisperPipline(f"openai/whisper-{model}")

    # JIT compile the forward call - slow, but we only do once
    print('JIT compile the forward call - slow, but we only do once')
    text = pipeline(input, language=language, return_timestamps=True)
    print(text)
    print(datetime.now()-start)

    start=datetime.now()
    # used cached function thereafter - super fast!!
    print('used cached function thereafter - super fast!!')
    text = pipeline(input, language=language, return_timestamps=True)
    print(text)
    print(datetime.now()-start)


if __name__ == '__main__':
    main()
