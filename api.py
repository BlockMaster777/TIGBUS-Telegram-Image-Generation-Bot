# coding=utf-8
""""
"""
import base64
import json
import time

import requests


class FusionBrainAPI:
    
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {'X-Key': f'Key {api_key}', 'X-Secret': f'Secret {secret_key}', }
    
    
    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']
    
    
    def generate(self, prompt, pipeline_id, images=1, width=1024, height=1024, style="NO STYLE", negative=""):
        params = {"type": "GENERATE", "numImages": images, "width": width, "height": height, "style": style, "negativePromptDecoder": negative,
                  "generateParams": {"query": f"{prompt}"}}
        data = {'pipeline_id': (None, pipeline_id), 'params': (None, json.dumps(params), 'application/json')}
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']
    
    
    def check_generation(self, request_id, attempts=10, delay=3):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                files = data['result']['files'][0]
                decoded = base64.b64decode(files)
                with open("result.png", "wb") as f:
                    f.write(decoded)
                return 0
            else:
                print(data["status"])
            attempts -= 1
            time.sleep(delay)
        return None