#!/usr/bin/env python
import whisper
import sys
import json
import os.path
import mimetypes

model = whisper.load_model("base")

for filename in sys.argv[1:]:
    output_filename = f"{filename}.whisper.json"
    if os.path.isfile(output_filename):
        continue
    mimetype, encoding = mimetypes.guess_type(filename)
    if not mimetype or not mimetype.startswith('video'):
        continue
    print(f"{filename}: {mimetype}")
    try:
        result = model.transcribe(filename)
    except:
        print(f"processing failed for {filename}")
        continue
    print(result['text'])
    with open(output_filename, "w+") as f:
        print(f"{filename} -> {output_filename}")
        json.dump(result, f, indent=4)
