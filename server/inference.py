import requests
import re

import io
import base64
from PIL import Image

# Settings
system_prompt = "You are watching a livestream on instagram."
instruction = "Based on the scene in the livestream, write 20 comments that people can write while viewing this livestream. Only write the list, nothing else. Make the comments short, with variety and without emoji's."


# -----------------------------------------------------------------


# Convert the LLM inference list into a python list
def array_from_out(input_string):

    # Use a regular expression to extract the text within quotation marks
    pattern = r'"(.*?)"'
    matches = re.findall(pattern, input_string)
    
    return matches



def generate_comments(b64image_data):

    #prompt = f"<|im_start|>system\n{system_prompt}\n<|im_end|>\n<|im_start|>instruction\n{instruction}\n<|im_end|>\n<|im_start|>assistant\n"
    prompt = f"<|im_start|>system\n{system_prompt} {instruction}\n<|im_end|>\n<|im_start|>assistant\n"

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

    # Create list from the text the LLM produced, and return it
    comment_list = array_from_out(response)
    return comment_list
