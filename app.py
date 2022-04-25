import os
import shutil
import gradio as gr
from PIL import Image
import subprocess

#os.chdir('Restormer')

# Download sample images
os.system("wget https://github.com/swz30/Restormer/releases/download/v1.0/sample_images.zip")
shutil.unpack_archive('sample_images.zip')
os.remove('sample_images.zip')


examples = [['project/cartoon2.jpg','project/video1.mp4'],
						['project/cartoon3.jpg','project/video2.mp4'],
						['project/celeb1.jpg','project/video1.mp4'],
						['project/celeb2.jpg','project/video2.mp4'],
						]

title = "DaGAN"
description = """
Gradio demo for <b>Depth-Aware Generative Adversarial Network for Talking Head Video Generation</b>, CVPR 2022L. <a href='https://arxiv.org/abs/2203.06605'>[Paper]</a><a href='https://github.com/harlanhong/CVPR2022-DaGAN'>[Github Code]</a>\n 
"""
##With Restormer, you can perform: (1) Image Denoising, (2) Defocus Deblurring, (3)  Motion Deblurring, and (4) Image Deraining. 
##To use it, simply upload your own image, or click one of the examples provided below.

article = "<p style='text-align: center'><a href='https://arxiv.org/abs/2203.06605'>Depth-Aware Generative Adversarial Network for Talking Head Video Generation</a> | <a href='https://github.com/harlanhong/CVPR2022-DaGAN'>Github Repo</a></p>"


def inference(img, video):
    if not os.path.exists('temp'):
      os.system('mkdir temp')
    ####  Resize the longer edge of the input image
    cmd = f"ffmpeg -y -ss 00:00:00 -i {video} -to 00:00:08 -c copy temp/driving_video.mp4"
    subprocess.run(cmd.split())
    driving_video = "video_input.mp4"
    os.system("python demo_dagan.py --source_image {} --driving_video 'temp/driving_video.mp4' --output 'temp/rst.mp4'".format(img))
    return f'temp/rst.mp4'
    
gr.Interface(
		inference,
		[
				gr.inputs.Image(type="filepath", label="Source Image"),
				gr.inputs.Video(type='mp4',label="Driving Video"),
		],
		gr.outputs.Video(type="mp4", label="Output Video"),
		title=title,
		description=description,
		article=article,
		theme ="huggingface",
		examples=examples,
		allow_flagging=False,
		).launch(debug=False,enable_queue=True)
