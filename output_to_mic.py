
import soundfile as sf
import sounddevice as sd
import json
import requests
import argparse

# Open the JSON file and load its contents into a dictionary
with open('settings.config', 'r') as file:
    setting = json.load(file)
PATH2RESULT = setting["path_for_result"]
FILE_NAME = setting["WAVE_OUTPUT_FILENAME"]
OUTPUT_DEVICE_NAME = setting["output_device"]

def send2Change():
    # URL of the Flask app
    url = 'http://10.0.0.217:6842/voiceChangeModel'
    parser = argparse.ArgumentParser(description='sovits4 inference')

    parser.add_argument('-cr', '--cluster_infer_ratio', type=float, default=0, help='聚类方案占比，范围0-1，若没有训练聚类模型则填0即可')
    parser.add_argument('-cm', '--cluster_model_path', type=str, default="logs/44k/kmeans_10000.pt", help='聚类模型路径，如果没有训练聚类则随便填')
    parser.add_argument('-sd', '--slice_db', type=int, default=-50, help='默认-40，嘈杂的音频可以-30，干声保留呼吸可以-50')
    parser.add_argument('-ns', '--noice_scale', type=float, default=0.4, help='噪音级别，会影响咬字和音质，较为玄学')
    parser.add_argument('-p', '--pad_seconds', type=float, default=0.5, help='推理音频pad秒数，由于未知原因开头结尾会有异响，pad一小段静音段后就不会出现')
    parser.add_argument('-wf', '--wav_format', type=str, default='flac', help='音频输出格式')

    args = parser.parse_args()

    slice_db = args.slice_db
    wav_format = args.wav_format
    cluster_infer_ratio = args.cluster_infer_ratio
    noice_scale = args.noice_scale
    pad_seconds = args.pad_seconds
    cluster_model_path = args.cluster_model_path

    # Data to be sent in the request
    data = {
        "slice_db":                 slice_db,
        "wav_format":               wav_format,
        "cluster_infer_ratio" :     cluster_infer_ratio,
        "cluster_model_path":       cluster_model_path,
        "noice_scale" :             noice_scale,
        "pad_seconds" :             pad_seconds,
    }

    # Sending a POST request with the data
    response = requests.post(url, data=data)

    # Checking the response status code
    if response.status_code == 200:
        # voice changed, push to mic
        push2MIC()
    else:
        # Printing the error message if the request fails
        print('Error:', response)

def push2MIC():
    # Load the audio file
    filename = PATH2RESULT + FILE_NAME + ".flac"
    data, fs = sf.read(filename)

    # Make sure the audio has only 1 channel
    if data.ndim > 1:
        data = data[:, 0]

    # Make sure the audio is 16-bit
    if data.dtype != "int16":
        data = (data * 32767).astype("int16")

    # Get a list of available audio devices
    devices = sd.query_devices()
    output_device_idx = None

    # Find the index of the virtual output device
    for idx, device in enumerate(devices):
        if device['name'] == OUTPUT_DEVICE_NAME:
            output_device_idx = idx
            break

    # Check if the virtual output device was found
    if output_device_idx is None:
        print(f"Error: Virtual output device '{OUTPUT_DEVICE_NAME}' not found.")
        exit()

    # Play the audio file through the virtual output device
    print(f"Playing '{filename}' through '{OUTPUT_DEVICE_NAME}'...")
    sd.play(data, fs, device=output_device_idx)

    # Wait for the audio to finish playing
    sd.wait()

if __name__ == "__main__":
    send2Change()