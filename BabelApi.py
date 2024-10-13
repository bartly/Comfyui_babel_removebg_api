import os
import io
import json
import requests
from io import BytesIO
from PIL import Image
import sys
import torch
import numpy as np
import base64

p = os.path.dirname(os.path.realpath(__file__))

globalAccessToken = ''

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def getBabelAccessToken():
    try:
        global globalAccessToken
        if globalAccessToken != '':
            return globalAccessToken
        config_path = os.path.join(p, 'config.json')
        with open(config_path, 'r') as f:  
            config = json.load(f)
        apikey = config["BABEL_KEY"]
        apisecret = config["BABEL_SECRET"]

        if apikey == '' or apisecret == '':
            raise Exception(f"apikey and apisecret is neccessary")

        response = requests.post(
            f"https://removebg-api.babel-hz.com/oauth/token",
            headers={
                "accept": "application/json",
            },
            json={
                "grantType":"client_credentials",
                "apikey":apikey,
                "apisecret":apisecret          
            },
        )

        if response.status_code == 200:
            jsonData = response.json()
            print(jsonData)
            if jsonData['code'] == 0:
                globalAccessToken = jsonData['data']['accessToken']
                return globalAccessToken
            else:
                print("Response Msg:", jsonData['msg'])
                raise Exception(f"Failed to fetch accessToken msg: {jsonData['msg']}") 
        else:
            print("Response Status Code:", response.status_code) 
            raise Exception(f"Failed to fetch accessToken status code: {response.status_code}")                

    except Exception as e:
        print(e)
        return ""


class BabelRemovebg:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_removebg"
    CATEGORY = "Babel/removebg/body"
                       
    def generate_removebg(self, image=None):

        accessToken = getBabelAccessToken()

        image = tensor2pil(image)
        # 将图像转换为字节流
        image_byte_arr = io.BytesIO()
        image.save(image_byte_arr, format='JPEG', quality = 90)
        image_byte_arr = image_byte_arr.getvalue()
        # 将字节流编码为 base64
        imageBase64 = base64.b64encode(image_byte_arr).decode('utf-8')
        print(f"image size is {len(imageBase64)}")

        response = requests.post(
            f"https://removebg-api.babel-hz.com/task/cutoff/body",
            headers={
                "Authorization": f"accessToken {accessToken}",
                "accept": "application/json"
            },
            json={
                "imageData":imageBase64,
                "type":"foreground",
                "returnType":"url"
            },
        )

        if response.status_code == 200:
            jsonData = response.json()
            if jsonData['code'] == 0:
                taskId = jsonData['data']['taskId']
                foreground = jsonData['data']['foreground']
                response = requests.get(foreground)

                if response.status_code == 200:
                    imagefile = f"{taskId}.png"
                    with open(imagefile, "wb") as f:
                        f.write(response.content)
                    image_data = Image.open(imagefile)
                    output_t = pil2tensor(image_data)
                    os.remove(imagefile)                   
                    print(output_t.shape)
                    return (output_t,)
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")                

            else:
                print("Response Msg:", jsonData['msg'])
                raise Exception(f"Failed to removebg msg: {jsonData['msg']}") 
        else:
            print("Response Status Code:", response.status_code) 
            raise Exception(f"Failed to removebg status code: {response.status_code}")
        


NODE_CLASS_MAPPINGS = {
    "BabelRemovebg": BabelRemovebg,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BabelRemovebg": "Babel-Removebg",
}
