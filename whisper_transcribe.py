import whisper

model = whisper.load_model("tiny")
result = model.transcribe("/media/Videos/PXL_20240605_150920501.mp4")

print(result["text"])