import io
import logging
import json
import soundfile
import torch
import torchaudio
from flask import Flask, request, send_file
from flask_cors import CORS

from inference.infer_tool import Svc, RealTimeVC

from pathlib import Path

import librosa
import matplotlib.pyplot as plt
import numpy as np

from inference import infer_tool
from inference import slicer

app = Flask(__name__)

CORS(app)

logging.getLogger('numba').setLevel(logging.WARNING)
chunks_dict = infer_tool.read_temp("inference/chunks_temp.json")

# Open the JSON file and load its contents into a dictionary
with open('../settings.config', 'r') as file:
    setting = json.load(file)


@app.route("/voiceChangeModel", methods=["POST"])
def voice_change_model():
    request_form = request.form

    clean_names     = [setting["WAVE_OUTPUT_FILENAME"]]
    trans           = [setting["pitch_adjust"]]
    spk_list        = [setting["actor_name"]]
    auto_predict_f0 = bool(setting["auto_f0"])

    slice_db            = int(float(request_form.get("slice_db", 0)))
    wav_format          = request_form.get("wav_format", 0)
    cluster_infer_ratio = float(request_form.get("cluster_infer_ratio", 0))
    noice_scale         = float(request_form.get("noice_scale", 0))
    pad_seconds         = float(request_form.get("pad_seconds", 0))

    # svc_model = Svc(model_name, config_name, 'cuda')
    infer_tool.mkdir(["raw", "results"])
    infer_tool.fill_a_to_b(trans, clean_names)
    for clean_name, tran in zip(clean_names, trans):
        raw_audio_path = f"raw/{clean_name}"
        if "." not in raw_audio_path:
            raw_audio_path += ".wav"
        infer_tool.format_wav(raw_audio_path)
        wav_path = Path(raw_audio_path).with_suffix('.wav')
        chunks = slicer.cut(wav_path, db_thresh=slice_db)
        audio_data, audio_sr = slicer.chunks2audio(wav_path, chunks)

        for spk in spk_list:
            audio = []
            for (slice_tag, data) in audio_data:
                print(f'#=====segment start, {round(len(data) / audio_sr, 3)}s======')

                length = int(np.ceil(len(data) / audio_sr * svc_model.target_sample))
                if slice_tag:
                    print('jump empty segment')
                    _audio = np.zeros(length)
                else:
                    # padd
                    pad_len = int(audio_sr * pad_seconds)
                    data = np.concatenate([np.zeros([pad_len]), data, np.zeros([pad_len])])
                    raw_path = io.BytesIO()
                    soundfile.write(raw_path, data, audio_sr, format="wav")
                    raw_path.seek(0)
                    out_audio, out_sr = svc_model.infer(spk, tran, raw_path,
                                                        cluster_infer_ratio=cluster_infer_ratio,
                                                        auto_predict_f0=auto_predict_f0,
                                                        noice_scale=noice_scale
                                                        )
                    _audio = out_audio.cpu().numpy()
                    pad_len = int(svc_model.target_sample * pad_seconds)
                    _audio = _audio[pad_len:-pad_len]

                audio.extend(list(infer_tool.pad_array(_audio, length)))
            res_path = f'./results/{clean_name}.{wav_format}'
            soundfile.write(res_path, audio, svc_model.target_sample, format=wav_format)
    
    # good!
    return "200"


if __name__ == '__main__':
    actor_name = setting["actor_name"]
    path2Model = setting["path_for_FLASK_to_model"]

    # 启用则为直接切片合成，False为交叉淡化方式
    # vst插件调整0.3-0.5s切片时间可以降低延迟，直接切片方法会有连接处爆音、交叉淡化会有轻微重叠声音
    # 自行选择能接受的方法，或将vst最大切片时间调整为1s，此处设为Ture，延迟大音质稳定一些
    raw_infer = False

    # 每个模型和config是唯一对应的
    model_name = path2Model + actor_name + "/" + actor_name + ".pth"
    config_name = path2Model + actor_name + "/" + "config.json" 
    # model_name = "D:/sound_changer/so-vits-svc/models/tannhuaser/tannhauser.pth"
    # config_name = "D:/sound_changer/so-vits-svc/models/tannhuaser/config.json"
    svc_model = Svc(model_name, config_name, 'cuda')

    # 此处与vst插件对应，不建议更改
    app.run(port=6842, host="0.0.0.0", debug=False, threaded=False)
