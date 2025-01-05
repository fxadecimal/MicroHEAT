cd img
ffmpeg -y -framerate 10 -i heat_step_%04d.png -c:v libx264 -pix_fmt yuv420p heat_diffusion.mp4

