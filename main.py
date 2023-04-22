import json
from scipy.io.wavfile import write
from text import text_to_sequence
from models import SynthesizerTrn
import utils
import commons
import sys
import re
import torch
from torch import no_grad, LongTensor
from winsound import PlaySound
from translateBaidu import translate_baidu
from tools import *
from termcolor import colored
import configparser
import Config
from enum import Enum
from io import BytesIO
from typing import Tuple, List
import io
import numpy as np
from scipy.io.wavfile import write
import base64
from flask import Flask, request, jsonify
from common import *
app = Flask(__name__)

# gpu 加速
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if device.type == "cuda":
    print("已开启GPU加速!")

chinese_model_path = "./model/"
chinese_config_path = "./model/cn_config.json"
japanese_model_path = "./model/"
japanese_config_path = "./model/jp_config.json"
record_path = "./chat_record/"
character_path = "./characters/"

ini_config = configparser.ConfigParser()
ini_config.read('config.ini', encoding='utf-8')

def get_text(text, hps, cleaned=False):
    if cleaned:
        text_norm = text_to_sequence(text, hps.symbols, [])
    else:
        text_norm = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm

def get_label_value(text, label, default, warning_name='value'):
    value = re.search(rf'\[{label}=(.+?)\]', text)
    if value:
        try:
            text = re.sub(rf'\[{label}=(.+?)\]', '', text, 1)
            value = float(value.group(1))
        except:
            print(f'Invalid {warning_name}!')
            sys.exit(1)
    else:
        value = default
    return value, text

def get_label(text, label):
    if f'[{label}]' in text:
        return True, text.replace(f'[{label}]', '')
    else:
        return False, text

def get_audio_bytes(sampling_rate: int, audio: np.ndarray) -> bytes:
    """
    将音频数据转换为字节流。
    
    :param sampling_rate: 采样率，例如 44100
    :param audio: 一个包含音频数据的NumPy数组
    :return: 字节流，可以用于发送、保存或播放
    """
    # 使用 BytesIO 对象作为内存中的文件
    with io.BytesIO() as buffer:
        # 使用 scipy.io.wavfile.write 将音频数据写入内存文件
        write(buffer, sampling_rate, audio)
        
        # 获取内存文件的字节内容
        buffer.seek(0)
        audio_bytes = buffer.read()
    
    return audio_bytes


def audio_bytes_to_base64_string(audio_bytes: bytes) -> str:
    """
    将音频字节流转换为Base64编码的字符串。
    
    :param audio_bytes: 音频字节流
    :return: Base64编码的字符串
    """
    # 使用 base64 模块将字节流编码为 Base64 编码的字符串
    base64_string = base64.b64encode(audio_bytes).decode("utf-8")
    
    return base64_string



def generateSound(inputString: str, id: str, key:str, model_type: modelType):
    if '--escape' in sys.argv:
        escape = True
    else:
        escape = False

    if model_type == modelType.CHINESE_MODEL:
        model =  chinese_model_path + key + '/' + key + '.pth'
        config = chinese_config_path
        inputString = "[ZH]" + inputString + "[ZH]"
    elif model_type == modelType.JAPANESE_MODEL:
        model = japanese_model_path + key + '/' + key + '.pth'
        config = japanese_config_path

    hps_ms = utils.get_hparams_from_file(config)
    n_speakers = hps_ms.data.n_speakers if 'n_speakers' in hps_ms.data.keys() else 0
    n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
    emotion_embedding = hps_ms.data.emotion_embedding if 'emotion_embedding' in hps_ms.data.keys() else False

    net_g_ms = SynthesizerTrn(
        n_symbols,
        hps_ms.data.filter_length // 2 + 1,
        hps_ms.train.segment_size // hps_ms.data.hop_length,
        n_speakers=n_speakers,
        emotion_embedding=emotion_embedding,
        **hps_ms.model)
    _ = net_g_ms.eval()
    utils.load_checkpoint(model, net_g_ms)

    if n_symbols != 0:
        if not emotion_embedding:
            #while True:
            if(1 == 1):
                choice = 't'
                if choice == 't':
                    text = inputString
                    if text == '[ADVANCED]':
                        text = "我不会说"

                    length_scale, text = get_label_value(
                        text, 'LENGTH', 1, 'length scale')
                    noise_scale, text = get_label_value(
                        text, 'NOISE', 0.667, 'noise scale')
                    noise_scale_w, text = get_label_value(
                        text, 'NOISEW', 0.8, 'deviation of noise')
                    # length_scale = 1
                    # noise_scale = 0.667
                    # noise_scale_w = 0.8
                    cleaned, text = get_label(text, 'CLEANED')

                    stn_tst = get_text(text, hps_ms, cleaned=cleaned)

                    speaker_id = id
                    out_path = "output.wav"

                    with no_grad():
                        x_tst = stn_tst.unsqueeze(0)
                        x_tst_lengths = LongTensor([stn_tst.size(0)])
                        sid = LongTensor([speaker_id])

                        # GPU 加速
                        x_tst = x_tst.to(device)
                        x_tst_lengths = x_tst_lengths.to(device)
                        sid = sid.to(device)
                        net_g_ms = net_g_ms.to(device)

                        audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale,
                                               noise_scale_w=noise_scale_w, length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()
                # write(out_path, hps_ms.data.sampling_rate, audio)
                return get_audio_bytes(hps_ms.data.sampling_rate, audio)
    return None

# 文字转声音二进制文件
def text_to_sound(model_type: modelType, model_id: Enum, text: str) -> str:
    id, key = Config.getModel(model_type.value, model_id.value)
    ret = generateSound(text, id, key, model_type)
    if not ret:
        return None
    return audio_bytes_to_base64_string(ret)

@app.route('/text_to_sound', methods=['GET'])
def text_to_sound_api():
    model_type = request.args.get('model_type')
    model_id = request.args.get('model_id')
    text = request.args.get('text')
    translate = request.args.get('trans')

    if not model_type or not model_id or not text:
        return jsonify({'error': 'Missing required parameters.'}), 400

    try:
        if int(translate) == 1:
            text = translate_baidu(text, ini_config.get('API', 'baidu_appid'), ini_config.get('API', 'baidu_secretKey'))
    except ValueError:
        return jsonify({'error': 'translate text failed.'}), 400
    
    try:
        model_type = modelType(int(model_type))
        if model_type == modelType.JAPANESE_MODEL:
            model_id = jpModelId(int(model_id))
        else :
            model_id = cnModelId(int(model_id))
    except ValueError:
        return jsonify({'error': 'Invalid model_type or model_id value.'}), 400

    base64_string = text_to_sound(model_type, model_id, text)
    if not base64_string:
        return jsonify({'error': 'Failed to generate sound.'}), 500

    return jsonify({'sound': base64_string})

if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == "__main__":
#     # 读取配置文件
#     config = configparser.ConfigParser()
#     config.read('config.ini', encoding='utf-8')

#     Config.checkApi(config)
#     text_to_sound(modelType.JAPANESE_MODEL, jpModelId.Kongqi_Rina, "こんにちは")
#     text_to_sound(modelType.CHINESE_MODEL, cnModelId.Delisa, "你好，旅行者！")
#     PlaySound(r'.\output.wav', flags=1)
#     input()