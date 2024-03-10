import openai
import json
import re


dataset = {}
openai.api_key = "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"

def create_question(text):
    prompt="Напиши вопрос к этому тексту: " + f"\n\n{text}"
    completions = openai.Completion.create(
        engine="gpt-3.5-turbo-0125",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return completions.choices[0].text


def split_text(file):
    json_dict = []
    for i in range(len(file)):
        if i > len(file)//2:
            break
        else:       
        # Разделение текста на предложения
            text = file[str(i+1)]
            sentences = text.split('. ')
    
    # Разделение предложений на части по 8
            parts = [sentences[i:i+8] for i in range(0, len(sentences), 8)]
    
    # Преобразование частей в строки и запись в словарь

            for part in parts:
                str_var_value = '. '.join(part)
                if str_var_value != "":
                    json_dict.append({"Вопрос": create_question(str_var_value)})
                    json_dict.append({"Ответ": str_var_value})
    
    return json_dict

with open("not_filter_data.json", "r",  encoding='utf-8') as f:
    file = json.load(f)


data = split_text(file)
    
with open("dataset.json", "a", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.write("\n")
