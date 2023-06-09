- ## MemeCam_ChatGPT 微信小程序爆梗相机源码

MemeCam_ChatGPT 是一个开源的微信小程序项目，它集成了图像识别技术（BLIP）和OpenAI的强大的自然语言处理引擎（GPT-4）。
### 主要功能 
- **上传图片** ：用户可以上传任意图片。 
- **图片内容识别** ：通过使用BLIP识别技术，我们的程序可以准确地识别上传的图片中的内容。 
- **生成有趣的文字** ：识别完图片内容之后，程序会使用ChatGPT生成与图片内容相关的有趣的文字。 
- **文字叠加** ：生成的文字会被叠加在用户上传的图片上，形成一种新颖的、有趣的视觉效果。
### 安装方式
一、后端部署
1.  下载项目backend到服务器
```
git clone https://github.com/smallnew666/MemeCam_ChatGPT.git
cd MemeCam_ChatGPT
pip3 install -r requirements.txt
```
2.  填写openai key
3.  运行程序
```
python3 index.py
```
本地接口地址为http://127.0.0.1:5000（如果是服务器，则修改为服务器ip）

二、前端部署

1.  下载小程序项目miniprogram到本地，微信开发者工具导入项目
2.  添加服务器端接口地址到url,
```
url: '替换为你的后端接口地址http:127.0.0.1/upload
```

### 演示地址

![Fp-wraSIIgkqX4xGGM1W8JUESd03](https://github.com/smallnew666/MemeCam_ChatGPT/assets/24582880/c494ecbb-e931-46b3-8c1f-57d7c6f85af1)
![，](https://github.com/smallnew666/MemeCam_ChatGPT/assets/24582880/eea5d73c-de99-41a9-a92a-81a0376de5e6)


### 联系我们

如果你有任何问题或建议，欢迎通过以下方式联系我们： 
- 微信群：mr_zabsa，备注拉群
- 获取更详细教程，欢迎加入知识星球，里面包括免费api key分享，chatgpt教程等相关内容
----

![2023-04-17 17 58](https://user-images.githubusercontent.com/24582880/233049472-8a731396-933a-4401-a773-f0ed58cc7b13.jpg)

MemeCam_ChatGPT - 让你的每一张图片都充满趣味！
