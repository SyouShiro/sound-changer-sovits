# Sound Changer using So-vits-svc

This repository contains an open source sound changer program that utilizes the [So-vits-svc](https://github.com/svc-develop-team/so-vits-svc) library to transform audio input.

## Installation

To install this program, you can clone the repository using Git:
```
git clone https://github.com/your-username/sound-changer-sovits.git
```
Then, navigate to the directory and install the dependencies using pip:
```
cd sound-changer-sovits
pip install -r requirements.txt
```
After than, navigate to the directory of so-vits-svc and replace its `flask_api.py` with this repo's `flask_api.py`.

This repo will assume you already installed so-vits-svc locally already.

## Usage
Edit the settings.config, make sure the path/actor/hotkey parameters were correct.

To use the sound changer program, run the following command:
```
python audio_record.py
```
Then, navigate to the directory of so-vits-svc and start the flask service by using python:
```
python flask_api.py
```

This will launch the program and start recording audio input. You can then choose from a list of sound transformation options using the settings.config, but there is more settings could be change in provided `flask_api.py`, mostly borrowed from so-vits-svc. Note that this program does not provide a pre-trained voice model. You will need to download or train your own voice model and use it with this program.

## Features

* Sound transformation using the [So-vits-svc](https://github.com/svc-develop-team/so-vits-svc) library
* Easy change of settings for sound transformation options
* Completely open source

## Contributing

If you'd like to contribute to this project, feel free to submit a pull request. You can also create issues if you encounter any bugs or have feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.