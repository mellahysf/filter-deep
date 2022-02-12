import cv2
import numpy as np
import os
import torch
from basicsr.utils import imwrite
from os.path import join, dirname, realpath

from gfpgan import GFPGANer

def inference(imgn):
    """Inference demo for GFPGAN.
    """
    #parser = argparse.ArgumentParser()
    #parser.add_argument('--upscale', type=int, default=2, help='The final upsampling scale of the image')
    #parser.add_argument('--arch', type=str, default='clean', help='The GFPGAN architecture. Option: clean | original')
    #parser.add_argument('--channel', type=int, default=2, help='Channel multiplier for large networks of StyleGAN2')
    #parser.add_argument('--model_path', type=str, default='../experiments/pretrained_models/GFPGANCleanv1-NoCE-C2.pth')
    #parser.add_argument('--bg_upsampler', type=str, default='realesrgan', help='background upsampler')
    #parser.add_argument(
    #    '--bg_tile', type=int, default=400, help='Tile size for background sampler, 0 for no tile during testing')
    #parser.add_argument('--test_path', type=str, default='../inputs/upload', help='Input folder')
    #parser.add_argument('--suffix', type=str, default=None, help='Suffix of the restored faces')
    #parser.add_argument('--only_center_face', action='store_true', help='Only restore the center face')
    #parser.add_argument('--aligned', action='store_true', help='Input are aligned faces')
    #parser.add_argument('--paste_back', action='store_false', help='Paste the restored faces back to images')
    #parser.add_argument('--save_root', type=str, default='../results', help='Path to save root')
    #parser.add_argument(
    #    '--ext',
    #    type=str,
    #    default='auto',
    #    help='Image extension. Options: auto | jpg | png, auto means using the same extension as inputs')
    suffix = None
    ext = "auto"
    #args = parser.parse_args()
    media_path = join(dirname(realpath(__file__)), 'media/')
    current_path = dirname(realpath(__file__))
    test_path = media_path + "inputs/upload"
    if test_path.endswith('/'):
        test_path = test_path[:-1]
    os.makedirs("media/results", exist_ok=True)
    bg_upsampler = "realesrgan"
    # background upsampler
    if bg_upsampler == 'realesrgan':
        if not torch.cuda.is_available():  # CPU
            import warnings
            warnings.warn('The unoptimized RealESRGAN is very slow on CPU. We do not use it. '
                          'If you really want to use it, please modify the corresponding codes.')
            bg_upsampler = None
        else:
            from basicsr.archs.rrdbnet_arch import RRDBNet
            from realesrgan import RealESRGANer
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
            bg_upsampler = RealESRGANer(
                scale=2,
                model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth',
                model=model,
                tile=400,
                tile_pad=10,
                pre_pad=0,
                half=True)  # need to set False in CPU mode
    else:
        bg_upsampler = None
    # set up GFPGAN restorer

    restorer = GFPGANer(
        model_path=current_path + "/experiments/pretrained_models/GFPGANCleanv1-NoCE-C2.pth",
        upscale=2,
        arch="clean",
        channel_multiplier=2,
        bg_upsampler=bg_upsampler)

    img_path = imgn
    print("imgnnnnnnnnnnnnnnnnnnnnn:", imgn)

    print("imaaaaaaaaaaaaaaaaaaaaaage path:", img_path)
        # read image
    img_name = os.path.basename(img_path)
    print("imaaaaaaaaaaaaaaaage name:", img_name)
    print(f'Processing {img_name} ...')
    basename, ext = os.path.splitext(img_name)
    print("imaaaaaaaaaaaaaaaaaaaaaage path:", img_path)
    input_img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # restore faces and background if necessary
    cropped_faces, restored_faces, restored_img = restorer.enhance(
        input_img, has_aligned=False, only_center_face=False, paste_back=True)
    #print("///////////////////:", restored_img)
    # save faces
    for idx, (cropped_face, restored_face) in enumerate(zip(cropped_faces, restored_faces)):
        # save cropped face
        save_crop_path = os.path.join(media_path + "results", 'cropped_faces', f'{basename}_{idx:02d}.png')
        imwrite(cropped_face, save_crop_path)
        # save restored face
        if suffix is not None:
            save_face_name = f'{basename}_{idx:02d}_{suffix}.png'
        else:
            save_face_name = f'{basename}_{idx:02d}.png'
        save_restore_path = os.path.join(media_path + "results", 'restored_faces', save_face_name)
        imwrite(restored_face, save_restore_path)
        # save comparison image
        cmp_img = np.concatenate((cropped_face, restored_face), axis=1)
        imwrite(cmp_img, os.path.join(media_path + "results", 'cmp', f'{basename}_{idx:02d}.png'))
    # save restored img
    if restored_img is not None:
        if ext == 'auto':
            extension = ext[1:]
        else:
            extension = ext
        if suffix is not None:
            save_restore_path = os.path.join(media_path + "results", 'restored_imgs',
                                             f'{basename}_{suffix}.{extension}')
        else:
            save_restore_path = os.path.join(media_path + "results", 'restored_imgs', f'{basename}.{extension}')
        imwrite(restored_img, save_restore_path)

    print(f'Results are in the [{"media/results"}] folder.')
    return save_restore_path


#if __name__ == '__main__':
#    inference()
