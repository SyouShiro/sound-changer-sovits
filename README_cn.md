# 基于 So-vits-svc 的变声器项目

[**English**](./README.md) | [**中文简体**](./README_cn.md)

这是一个开源的AI变声项目，使用 [So-vits-svc](https://github.com/svc-develop-team/so-vits-svc) 库来转换音频输入。


## 安装

要安装这个程序，你可以使用 Git 克隆代码库：
```
git clone https://github.com/your-username/sound-changer-sovits.git
```
然后，导航到目录并使用 pip 安装依赖项：
```
cd sound-changer-sovits
pip install -r requirements.txt
```
之后，导航到 [So-vits-svc](https://github.com/svc-develop-team/so-vits-svc) 的目录，并使用这个代码库提供的`flask_api.py`替换掉原本的`flask_api.py`。

这个代码库假定你已经在本地安装了[So-vits-svc](https://github.com/svc-develop-team/so-vits-svc)。


## 使用

编辑 `settings.config` 文件，确保 `path`、`actor`、`hotkey` 等参数正确。

要使用声音变声程序，请在目录下开启terminal运行以下命令：
```
python audio_record.py
```
然后，导航到 [So-vits-svc](https://github.com/svc-develop-team/so-vits-svc) 的目录，并使用 python 启动 flask 服务：
```
python flask_api.py
```

这将启动程序并开始记录音频输入。你可以在`settings.config`中选择一系列声音转换选项，但是还有更多的设置可以在提供的`flask_api.py`中进行更改，这大部分是借鉴自 [So-vits-svc](https://github.com/svc-develop-team/so-vits-svc)。

## 请注意，这个程序不提供已训练的语音模型。你需要下载或训练自己的语音模型，并将其与此程序一起使用。


## Features

* 使用 [So-vits-svc](https://github.com/svc-develop-team/so-vits-svc) 库进行声音变换
* 客制化，自定义，多种多样的声音任你选择
* 简单的设置选项，方便进行声音变换
* 完全开源


## 贡献

如果你想为这个项目做出贡献，可以提交一个拉取请求(PR)。如果你遇到任何 bug 或有功能请求，也可以创建问题(issue)。


## 许可证

这个项目使用 MIT 许可证 - 请参阅 [LICENSE](LICENSE) 文件以获取详情。