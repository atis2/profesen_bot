import os   
from openai import OpenAI
from config  import *
import sqlite3
import json
import time
import base64
from PIL import Image
from io import BytesIO
import requests


prompt = """1. 🧑‍💻 **Профессия 1**: Информация про профессию 1.

2. 📊 **Профессия 2**: Информация про профессию 2.

3. 🖥 **Профессия 3**: Информация про профессию 3.

4. 🌐 **Профессия 4**: Информация про профессию 4.

5. 🔍 **Профессия 5**: Информация про профессию 5."""



class Profeson:

    def __init__(self ):
        self.client = OpenAI(
            api_key= SamKey,  # This is the default and can be omitted
        )
    
    def Ai_start(self,text):
        question = text
        chat_completion = self.client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Пришли 5 профессии по этим инструкциям: " + question + " Эти сообщения, которые ты генерируешь, отправляются в телеграм, стилизуй их, но не добавляй ничего лишнего. Не пиши лишних команд через / и т.д. Делай как тут: " + prompt,
        }
    ],
    model="gpt-4o",
)
        return(chat_completion.choices[0].message.content)




def create_tables():
    db = sqlite3.connect(database)
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS status(id INTEGER PRIMARY KEY, name TEXT, preferences TEXT)")
    db.commit()
    db.close()

def add_info(name , pr):
    db = sqlite3.connect(database)
    with db:
        db.execute('DELETE FROM status WHERE name = ?' ,(name,))
        db.execute('INSERT INTO status(name, preferences) VALUES( ?, ?)' ,(name, pr))
        db.commit()



def get_info(name):
    db = sqlite3.connect(database)
    with db:
        cur = db.cursor()
        cur.execute('SELECT preferences FROM status WHERE name = ?' ,(name,))
        dbText = cur.fetchall()
        return dbText [0][0]


class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=60, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
def show(prompt):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'EB9DF08F312BD7134EC9E8B1AA53AB00', 'B57D2C9556A05074ED4E9EEECEC3AF14')
    model_id = api.get_model()
    uuid = api.generate(f"{prompt}", model_id)
    images = api.check_generation(uuid)[0]  
    
    if images.startswith("data:image"):
        images = images.split(",")[1]

    image_data = base64.b64decode(images)
    with open("output_image.png", "wb") as f:
        f.write(image_data)
    return "output_image.png"

if __name__ == '__main__':
    pro = get_info("LopAtikkkk")
    print(pro)
    