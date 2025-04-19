# step 1

extract keyframes:

ffmpeg -skip_frame nokey -i  /media/Videos/PXL_20240314_232208947.mp4 -vsync 0 -r 30 -f image2 thumbnails-%02d.jpeg

# step 2

extract faces from keyframes:

python extract.py -i thumbnails-01.jpeg

# step 3

cluster faces

# step 4

human labeling

# step 5

create lists based on face - video
