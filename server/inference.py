import requests
import re

import io
import base64
from PIL import Image


# Settings
system_prompt = "You are watching a livestream on instagram."
instruction = "based on the scene in the livestream, write 20 comments that people can write while viewing this livestream. make them short, with variety and without emoji's."
format_style = ""

# -----------------------------------------------------------------

# Conver a png to base64 code
def img_to_b64(img_string):

    # Save and open image         
    image = Image.open(img_string)

    # Create a byte buffer
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='PNG')
    byte_content = byte_arr.getvalue()

    # Encode the byte content as base64
    base64_bytes = base64.b64encode(byte_content)
    base64_string = base64_bytes.decode('utf-8')

    return base64_string


# Convert a text list into a python list
def array_from_out(input_string):

    # Use a regular expression to extract the text within quotation marks
    pattern = r'"(.*?)"'
    matches = re.findall(pattern, input_string)
    
    return matches



def generate_comments(b64image_data):

    prompt = f"<|im_start|>system\n{system_prompt}\n<|im_end|>\n<|im_start|>instruction\n{instruction}\n<|im_end|>\n<|im_start|>assistant\n"

    # Data to send to the API
    data = {
        "prompt": prompt, 
        "images": [b64image_data], 
        "temperature": 0.1,
        "max_context_length": 4096, 
        "max_length": 512, 
        "top_p": 0.92, 
        "min_p": 0,
        "top_k": 100, 
        "top_a": 0, 
        "rep_pen": 1.1,  
        "sampler_order": [6, 0, 1, 3, 4, 2, 5],
        "stop_sequence": ["<|im_end|>", "<|end|>"], 
        "trim_stop": True,
    }

    # Send a request to the API to generate using our data
    response = requests.post("http://localhost:5001/api/v1/generate", json=data)
    response = response.json()["results"][0]["text"].strip()

    comment_list = array_from_out(response)
    print(comment_list)
