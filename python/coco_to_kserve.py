import os
import json
import numpy as np
from PIL import Image


def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def to_kserve(image_path, output_path):
    # Load image
    im = Image.open(image_path)

    # Pad to 640x640 square
    im = expand2square(im, (0, 0, 0))

    # Convert to np array of correct shape
    arr = np.transpose(np.array(im), (2, 0, 1))
    arr = np.expand_dims(arr, axis=0)

    # Write to json
    row = {"name": "images", "shape": arr.shape, "datatype": "FP32", "data": arr.tolist()}
    datajson = {"inputs": [row]}

    # Create the output filename
    file_name = os.path.basename(image_path)
    outname = os.path.splitext(file_name)[0] + ".json"
    output_file_path = os.path.join(output_path, outname)

    with open(output_file_path, "w") as outfile:
        json.dump(datajson, outfile)

    return outname
