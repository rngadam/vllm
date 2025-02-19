# What it is

We use [vit-gpt2-image-captioning](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning)

## Usage

```
MEDIADIR=/media/Videos
# generate a thumbnail for each file with video content in the directory that does not already have a thumbnail
./generate_thumbnails.sh $MEDIADIR/*
# generate a one-liner caption for each thumbnail that does not already have a thumbnail
python vit-gpt2-image-captioning.py $MEDIADIR/*thumbnail.jpg
```

## output example:

```
/media/Videos/1535556432780.mp4.thumbnail.jpg: a bird perched on top of a tree branch
/media/Videos/1535556457872.mp4.thumbnail.jpg: a bird perched on top of a tree branch
/media/Videos/1535556475134.mp4.thumbnail.jpg: a man is painting a statue of an elephant
/media/Videos/1535556493427.mp4.thumbnail.jpg: a young man sitting on a bench in a park
/media/Videos/1535556561152.mp4.thumbnail.jpg: a woman with glasses sitting on a bench
```