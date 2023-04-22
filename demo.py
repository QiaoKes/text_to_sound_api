import requests
import base64
import json
import binascii
from common import *

def save_binary_to_file(binary_data, filename):
    """
    将二进制数据保存为文件。
    
    :param binary_data: 二进制数据
    :param filename: 保存的文件名
    """
    with open(filename, 'wb') as file:
        file.write(binary_data)

def request_text_to_sound(model_type: int, model_id: int, text: str, trans: bool = False) -> bytes:
    """
    向RESTful API发起请求，将文本转换为声音的二进制数据。
    
    :param model_type: 模型类型的整数值
    :param model_id: 模型ID的整数值
    :param text: 要转换为声音的文本
    :return: 音频字节数据，如果请求失败则返回 None
    """
    base_url = "http://localhost:5000"
    url = f"{base_url}/text_to_sound?model_type={model_type}&model_id={model_id}&text={text}&trans={int(trans)}"
    
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Request failed due to a network error: {e}")
        return None

    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}.")
        return None

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Failed to decode API response as JSON.")
        return None

    base64_string = data.get('sound')

    if not base64_string:
        print("Failed to get sound from API response.")
        return None

    try:
        audio_bytes = base64.b64decode(base64_string.encode("utf-8"))
    except (binascii.Error, TypeError) as e:
        print(f"Failed to decode Base64 string to bytes: {e}")
        return None

    return audio_bytes

# 示例使用
model_type = modelType.JAPANESE_MODEL.value
model_id = jpModelId.Jinghua.value
text = "你好啊，旅行者！"
audio_bytes = request_text_to_sound(model_type, model_id, text, True)

if audio_bytes:
    print("Received audio bytes:", audio_bytes)
else:
    print("Failed to get sound.")
    exit()

save_binary_to_file(audio_bytes, "out.wav")