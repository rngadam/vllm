# What it is

Set of scripts to generate thumbnails, captions and transcribe audio of videos

## Implementation

* ffmpeg: thumbnail extraction
* [vit-gpt2-image-captioning](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning) to generate captions from a single I-frame thumbnail.
* [whisper](https://github.com/openai/whisper) for audio transcription

## Usage

There's a set of scripts that generate output files until ultimately it gets uploads in batch.

```bash
MEDIADIR=/media/Videos
# generate a thumbnail for each file with video content in the directory that does not already have a thumbnail
# (videos are autodetected, other filetypes rejected)
./generate_thumbnails.sh $MEDIADIR/*

# generate a one-liner caption for each thumbnail that does not already have a thumbnail
python vit-gpt2-image-captioning.py $MEDIADIR/*thumbnail.jpg

# generate a transcription of the video audio
# (videos are autodetected)
./whisper_transcribe.py $MEDIADIR/*

# upload all videos
# (videos must have thumbnail, transcription, caption)
./uploads.sh $MEDIADIR/*
```
