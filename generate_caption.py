# /hpc2hdd/home/jhe307/Project/Datasets/datasets--AI4Math--MathVista/snapshots/2b6ad69445fbb5695c9b165475e8decdbeb97747/images.zip
# Describe the specific information in the math picture
# 

import os
import zipfile
import json
import requests
import tempfile
import time

# GPT-4o API 配置
API_URL = "https://api2.aigcbest.top/v1/chat/completions"
API_KEY = "sk-dpyfnX02Xa6Zk5llXUmNTxrtZ6YaAya404EhUSw1OR3cVLXV"  # 替换为你的 API 密钥

def get_image_description(image_url, retries=3):
    headers = {
        'Accept': 'application/json',
        'Authorization': API_KEY,
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    # 准备请求数据
    payload = json.dumps({
        "model": "gpt-4o",
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe the specific information in the math picture"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        "temperature": 0.9,
        "max_tokens": 400
    })

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, data=payload)
            response.raise_for_status()  # 检查响应状态
            result = response.json()
            description = result['choices'][0]['message']['content']
            return description
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{retries} failed: {e}")
            time.sleep(2)  # 等待一段时间再重试
            
    return None

def main(zip_file_path, output_json_path):
    descriptions = {}
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 遍历 ZIP 文件中的图片
        for idx, file_name in enumerate(zip_ref.namelist()):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # 仅处理图片文件
                with zip_ref.open(file_name) as file:
                    # 创建临时文件
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as temp_file:
                        temp_file.write(file.read())  # 将图片写入临时文件
                        temp_file_path = temp_file.name  # 获取临时文件路径
                        
                # 生成 file:// URL
                image_url = f"file://{temp_file_path}"
                
                # 获取描述
                description = get_image_description(image_url)
                
                if description:
                    descriptions[f"image_{idx + 1}"] = description

    # 将描述写入 JSON 文件
    with open(output_json_path, 'w') as json_file:
        json.dump(descriptions, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    zip_file_path = "MathAgent/images.zip"  # 替换为你的 ZIP 文件路径
    output_json_path = "descriptions.json"  # 输出 JSON 文件路径
    main(zip_file_path, output_json_path)