import os
import click
from dotenv import load_dotenv
from .main import add_subtitles_to_video

@click.command()
@click.option('--input', '-i', required=True, help='Path to video file', type=click.Path(exists=True))
@click.option('--output', '-o', required=True, help='Output video file', type=click.Path())
@click.option('--api_key', required=False, help='AssemblyAI API key', type=str, default=None)
def auto_subtitles(input, output, api_key):
    if api_key is None:
        load_dotenv()
        if 'AAI_API_KEY' not in os.environ:
            raise ValueError('No API key provided')
    else:
        os.environ['AAI_API_KEY'] = api_key
        
    add_subtitles_to_video(input, output)