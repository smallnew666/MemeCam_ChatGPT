#from flask_cors import CORS
import openai
import base64
import io
import json
from PIL import Image, ImageDraw, ImageFont
#import replicate
import base64
import requests
import imghdr
from io import BytesIO
import time
from models.blip import blip_decoder
from PIL import Image
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
from flask import Flask, request,send_file
import os
import uuid
import datetime

app = Flask(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


@app.route('/')
def hello_world():  # put application's code here
    a = 'Welcom!'
    return a


@app.route('/upload', methods=['POST'])
def upload():
    #第三方接口
    image = request.files['image']
    image_file = image.read()
    #file_type = file.content_type.split('/')[1]   # 获取上传文件的格式
    #file_data = file.read()
    image_size = 350
    image = load_demo_image(image_file,image_size=image_size, device=device)

    model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth'
        
    model = blip_decoder(pretrained=model_url, image_size=image_size, vit='base')
    model.eval()
    model = model.to(device)

    with torch.no_grad():
        # beam search
        #caption = model.generate(image, sample=False, num_beams=9, max_length=20, min_length=5) 
        # nucleus sampling
        caption = model.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5) 
        print('caption: '+caption[0])
    text = caption[0]
    openai.api_key = "sk-***" #修改这里为自己申请的api_key
    messages = [
        {"role": "system", "content": "你是一个中文模因专家，您可以从描述中生成简短的讽刺模因字幕,请用中文回复。下面是我的描述:"},
    ]
    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0,
        stream=False  # again, we set stream=True
    )
    generated_text = response["choices"][0]["message"].content
    print(generated_text)
    #image_path = "cat.jpg"
    # 示例用法
    n = ImgText(generated_text,image_file)
    res = n.draw_text()
    json_data = {'data':  "https://nginx-web-fraork-njcq-uwcqowzevm.cn-chengdu.fcapp.run"+res}
    json_img = json.dumps(json_data)
    print(json_img)
    return json_img
def load_demo_image(image_file, image_size, device):
    # 将图像转换为PIL Image对象
    image = Image.open(io.BytesIO(image_file))
    # 将图像转换为RGB格式
    raw_image = image.convert("RGB")

    transform = transforms.Compose([
        transforms.Resize((image_size, image_size), interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
    ])
    image = transform(raw_image).unsqueeze(0).to(device)

    # 打印张量形状以进行调试
    print(f"Image tensor shape: {image.shape}")

    return image
class ImgText:
    font = ImageFont.truetype("kuaikanshijieti.ttf",50)

    def __init__(self, text,image):
        # 预设宽度 可以修改成你需要的图片宽度
        #img = Image.open(image)
        img = Image.open(io.BytesIO(image))
        width = img.size[0]
        height = img.size[1]
        print(width)
        self.width = width
        self.height = height
        # 文本
        self.text = text
        self.image = image
        # 段落 , 行数, 行高
        self.duanluo, self.note_height, self.line_height = self.split_text()

    def get_duanluo(self, text):
        txt = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        # 所有文字的段落
        duanluo = ""
        # 宽度总和
        sum_width = 0
        # 几行
        line_count = 1
        # 行高
        line_height = 0
        for char in text:
            #width, height = draw.textsize(char, ImgText.font)
            # 使用 textbbox 获取文本的坐标
            bbox = draw.textbbox((0, 0), char, font=ImgText.font)
            # 计算文本的宽度和高度
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            sum_width += width
            if sum_width > self.width:  # 超过预设宽度就修改段落 以及当前行数
                line_count += 1
                sum_width = 0
                duanluo += '\n'
            duanluo += char
            line_height = max(height, line_height)
        if not duanluo.endswith('\n'):
            duanluo += '\n'
        return duanluo, line_height, line_count

    def split_text(self):
        # 按规定宽度分组
        max_line_height, total_lines = 0, 0
        allText = []
        for text in self.text.split('\n'):
            duanluo, line_height, line_count = self.get_duanluo(text)
            max_line_height = max(line_height, max_line_height)
            total_lines += line_count
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height
        return allText, total_height, line_height

    def draw_text(self):
        """
        绘图以及文字
        :return:
        """
        note_img = Image.open(io.BytesIO(self.image)).convert("RGB")
        draw = ImageDraw.Draw(note_img)
        # 左上角开始
        x, y = 0, int(self.height)/2
        for duanluo, line_count in self.duanluo:
            #draw.text((x, y), duanluo, fill=(255, 255, 255), font=ImgText.font)
            #draw.text((x, y), duanluo, fill=(255, 255, 255), font=ImgText.font)
            draw.text((x+2, y), duanluo, fill=(0, 0, 0), font=ImgText.font)
            draw.text((x-2, y), duanluo, fill=(255, 255, 255), font=ImgText.font)
            draw.text((x, y+2), duanluo, fill=(0, 0, 0), font=ImgText.font)
            draw.text((x, y-2), duanluo, fill=(255, 255, 255), font=ImgText.font)
            y += self.line_height * line_count
        #note_img.save("result.png")
        
        '''
        buffer = io.BytesIO()
        note_img.save(buffer, format='png')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # 构建JSON数据对象，其中'data'字段包含base64编码的图像数据
        json_data = {'data':  f"data:image/png;base64,{img_base64}"}

        # 将JSON数据转换为字符串并打印
        json_img = json.dumps(json_data)
        '''
        # 获取当前日期
        today = datetime.date.today()

        # 按照日期生成目录
        dir_name = today.strftime('%Y-%m-%d')
        dir_path = os.path.join('/home/BLIP/imagedir', dir_name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        else:
            print('目录已存在，跳过生成')

        # 将文件保存到目录中
        # 生成随机的文件名
        filename = str(uuid.uuid4()) + '.jpg'
        note_img.save("./imagedir/"+dir_name+"/"+filename)
        os.chmod("./imagedir/"+dir_name+"/"+filename, 0o777)
        return "/imagedir/"+dir_name+"/"+filename



if __name__ == '__main__':
    app.run(threaded = False,processes=5,host="0.0.0.0",port="5000")