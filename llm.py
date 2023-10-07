import requests
import json


def llm(data):
    # https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md
    url = "http://localhost:8080/completion"
    headers = {"Content-Type": "application/json"}
    text = ""
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        text = response_data["content"]
        if response_data["stopped_word"]:
            text += response_data["stopping_word"]
    else:
        print(f"Request failed with status code {response.status_code}")
        return (None, None)
    return (text, response_data)


def tokenize(text):
    url = "http://localhost:8080/tokenize"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json={"content": text})
    if response.status_code == 200:
        response_data = json.loads(response.text)
        return response_data["tokens"]
    else:
        print(f"Request failed with status code {response.status_code}")
        return None
