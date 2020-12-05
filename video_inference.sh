#export VIDEO= ${1}  # change to your video file
#This script helps you to take a video input and Generate a overlayed output video
echo $1 $2
mkdir ${1}.images_${4}
ffmpeg -i ${1} -ss 00:00:00 -to 00:30:00 -vf fps=$2 ${1}.images_${4}/frame%04d.jpg -hide_banner
#ffmpeg -i ${VIDEO}  -qscale:v 2 -vf  fps=1 scale=641:-1 -f image2 ${VIDEO}.images/%05d.jpg
python3 main.py -i ${1}.images_${4} -mp ${3} -o test_data/${4}/output
ffmpeg -framerate $2 -pattern_type glob -i test_data/${4}/output/'*_output.jpg' -vf scale=640:-1 -c:v libx264 -pix_fmt yuv420p ${1}_${4}.mp4
rm -r ${1}.images_${4}
rm -r test_data/${4}/output/*
