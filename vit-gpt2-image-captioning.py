
# https://huggingface.co/nlpconnect/vit-gpt2-image-captioning
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import sys
import json
import os.path

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def predict_step(image_paths):
  images = []
  for image_path in image_paths:
    i_image = Image.open(image_path)
    if i_image.mode != "RGB":
      i_image = i_image.convert(mode="RGB")

    images.append(i_image)

  pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
  pixel_values = pixel_values.to(device)

  output_ids = model.generate(pixel_values, **gen_kwargs)

  preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
  preds = [pred.strip() for pred in preds]
  return preds

inputs = list(filter(lambda a: not os.path.isfile(a + '.caption.txt'), sys.argv[1:]))
if len(inputs) == 0:
    print("every inputs has a caption")
    sys.exit(1)

batch_size = 50
for i in range(0, len(inputs), batch_size):
  inputs_slice = inputs[i:i+batch_size]
  output = predict_step(inputs_slice)
  for filename, prediction in zip(inputs_slice, output):
      output_filename = filename + '.caption.txt'
      print(f"{filename}: {prediction}")
      with open(output_filename, 'w+') as f:
          f.write(prediction + '\n')