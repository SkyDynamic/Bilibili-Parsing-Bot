import json
import os

class Config_Read():
    def __init__(self):
        if not os.path.exists('data/bilitool'):
            os.makedirs('data/bilitool')
        if not os.path.exists('data/bilitool/data.json'):
            with open('data/bilitool/data.json','w',encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        with open('data/bilitool/data.json','r',encoding='utf-8') as f:
            self.group = json.load(f)

class Config_Write():
    def __init__(self, data):
        if os.path.exists('data/bilitool/data.json') == None:
            with open('data/bilitool/data.json','w',encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        with open('data/bilitool/data.json','w',encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)