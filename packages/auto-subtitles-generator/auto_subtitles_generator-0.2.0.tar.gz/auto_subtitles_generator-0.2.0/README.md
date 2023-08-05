# Auto-subtitles video tool using AssemblyAI API and ffmpeg

## Requirements

You need an AssemblyAI API key. You can get one [here](https://app.assemblyai.com/login).
API key can be set using the `--api_key` option or by setting the `AAI_API_KEY` environment variable.

## Install

### Pip

```bash
pip3 install auto-subtitles-generator
```

### From source

```bash
git clone 
cd auto-subtitles-generator
poetry install
```

## Usage

```bash
Usage: auto_subtitles [OPTIONS]

Options:
  -i, --input PATH   Path to video file  [required]
  -o, --output PATH  Output video file  [required]
  --api_key TEXT     AssemblyAI API key
  --help             Show this message and exit.
```

## Coverage

```bash
coverage run -m unittest && coverage report -m
```
