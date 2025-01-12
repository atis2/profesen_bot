import os   
from openai import OpenAI
from config  import *
import sqlite3


prompt = """1. 🧑‍💻 **Программист**: Пиши код и создавай программы, не выходя из дома.

2. 📊 **Аналитик данных**: Исследуй данные и получай инсайты, работая за своим компьютером.

3. 🖥 **Графический дизайнер**: Создавай впечатляющие визуальные решения, не покидая удобного домашнего пространства.

4. 🌐 **Веб-разработчик**: Строй современные веб-сайты и приложения, оставаясь в уюте своего дома.

5. 🔍 **Тестировщик ПО**: Проверяй качество программного обеспечения и выявляй баги, работая удаленно."""



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
        db.execute('INSERT INTO status(name, preferences) VALUES( ?, ?)' ,(name, pr))
        db.commit()






if __name__ == '__main__':
    pro = create_tables()
    