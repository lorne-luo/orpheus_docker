import click

from whisper_jax import FlaxWhisperPipline


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--language', '-l', default='zh', required=False, help='Language')
@click.option('--model', '-m', default='large-v2', required=False, help='Model file or data')
def main(input, language, model):
    # instantiate pipeline
    pipeline = FlaxWhisperPipline(f"openai/whisper-{model}")

    # used cached function thereafter - super fast!!
    text = pipeline(input, language=language, return_timestamps=True)
    print(text)

if __name__ == '__main__':
    main()