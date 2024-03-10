import json
import requests
from bs4 import BeautifulSoup
import colorama


data = {}

def import_text(link):
    page = requests.get(link).text
    soup = BeautifulSoup(page)
    p_tags = soup.find_all("p")
    #Обработка данных
    p_tags_text = [tag.get_text().strip() for tag in p_tags]
    sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
    sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
    # комбинирование полученных данных в одну str переменную
    article = ' '.join(sentence_list)
    return article

with open("states_Hubr.json", "r", encoding='utf-8') as f:
    file = json.load(f)


for i in range(len(file)):
    if i > (len(file)//2)-1:
       break
    else:
        data[i+1] = import_text(file[str(i+1)])
        
        
with open("data/not_filter_data.json", "w",  encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)