import base64
import time
from http.client import HTTPResponse
from io import BytesIO
from os.path import join, dirname, realpath

from flask import Flask, request, jsonify, Response
import werkzeug

from inference_gfpgan import inference
app = Flask(__name__)
import os
from flask import send_file

@app.route('/upload', methods=["POST"])
def upload():
    if request.method == "POST":

        deb = time.time()
        imagefile = request.files['file']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        print("\nReceived image File name : " + imagefile.filename)
        media_input_upload_path = join(dirname(realpath(__file__)), 'media/inputs/upload/')
        print("*******************************************************/////////////")

        imagefile.save(media_input_upload_path + filename)
        print("*******************************************************/////////////saved")
        ## TODO: Call model and get res_image
        ##!python inference_gfpgan.py --upscale 2 --test_path inputs/upload --save_root results --model_path experiments/pretrained_models/GFPGANCleanv1-NoCE-C2.pth --bg_upsampler realesrgan
        save_restore_path = inference(media_input_upload_path + filename)
        print("*******************************************************/////////////inference done")
        media_output_path = join(dirname(realpath(__file__)), save_restore_path)
        os.remove(media_input_upload_path + filename)
        fin = time.time()
        print("inference DONE************" + str(fin-deb))
        print("save_restore_path///////////" + save_restore_path)
        ## TODO: return the res_image, store it in json then remove it from results directory
        #return jsonify({
        #    ## TODO: return also the res_image
        #    "message": "Image Uploaded Successfully ",
        #})
        #with open(save_restore_path, "rb") as image_file:
        #    encoded_string = base64.b64encode(image_file.read())
        #with open(save_restore_path, "rb") as image_file:
        #    encoded_string = base64.b64encode(image_file.read())
        #print(HTTPResponse(str(save_restore_path).replace("\\", "/")))
        ## TODO: Response of restframewotk of DJANGO
        return Response(str(media_output_path))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
