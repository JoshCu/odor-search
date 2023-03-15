import os
import openai
import json
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarise_odor(odor_list):
    print("-"*30)
    print(odor_list)
    string_list = json.dumps(odor_list)    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=generate_prompts(string_list),
        temperature=0.6,
    )
    print(response)
    return response.choices[0].message.content


def generate_prompts(odor_list):
    messages = [{"role": "system", "content": """
    You are an odor character compiling machine and trained perfumer. 
    I provide you lists of lists of words describing the smell of a chemical,
     and you give me back one list of words that describe the chemicals odor.
     Do not include any word modifers for example: strongly, instensely, slight, faint.
     Do not include non-descriptive words like: odor, smell, fragrance, aroma, taste,etc."""},
                {"role": "system", "content": "Your response should just be the list, not a sentence or anything else."},
                {"role": "user", "content": f"{odor_list}"},]
    return messages
