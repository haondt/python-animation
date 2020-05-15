import glob
from PIL import Image

fp_in = 'tmp/frame_*.png'
fp_out = 'test3.gif'
fnames = sorted(glob.glob(fp_in), key=lambda x: int(''.join([i for i in x if i.isdigit()])))

img, *imgs = [Image.open(f) for f in fnames]

img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=20, loop=0)
