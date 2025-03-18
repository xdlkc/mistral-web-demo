import os
import base64
import json
import requests
from mistralai.client import MistralClient as MistralAPI
from mistralai.models.chat_completion import ChatMessage

class MistralClient:
    def __init__(self):
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY 环境变量未设置")
        self.model = "mistral-small-latest"  # 支持视觉功能
        self.client = MistralAPI(api_key=self.api_key)
        self.api_base = "https://api.mistral.ai/v1"
    
    def text_chat(self, messages):
        """处理纯文本对话"""
        chat_messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in messages]
        
        response = self.client.chat(
            model=self.model,
            messages=chat_messages
        )
        return response.choices[0].message.content
    
    def image_chat(self, messages, image_path):
        """处理包含图像的对话"""
        # 读取并编码图像
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 构建消息历史
        messages_for_api = []
        
        # 添加历史消息
        for i, msg in enumerate(messages):
            if i < len(messages) - 1:  # 不是最后一条消息
                messages_for_api.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # 添加带图像的最后一条消息
        last_msg = messages[-1]
        messages_for_api.append({
            "role": last_msg["role"],
            "content": [
                {
                    "type": "text",
                    "text": last_msg["content"]
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        })
        
        # 直接使用requests库进行API请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json={
                    "model": self.model,
                    "messages": messages_for_api
                }
            )
            response.raise_for_status()  # 检查HTTP错误
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"]
        except Exception as e:
            try:
                # 如果出错，尝试使用另一种格式
                messages_for_api[-1]["content"][-1]["image_url"] = {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                response = requests.post(
                    f"{self.api_base}/chat/completions",
                    headers=headers,
                    json={
                        "model": self.model,
                        "messages": messages_for_api
                    }
                )
                response.raise_for_status()
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"]
            except Exception as e2:
                # 记录详细错误信息
                error_msg = f"图像处理失败: {str(e)}"
                if hasattr(e, 'response') and e.response:
                    error_msg += f"\n响应状态: {e.response.status_code}"
                    error_msg += f"\n响应内容: {e.response.text}"
                
                second_error = f"{str(e2)}"
                if hasattr(e2, 'response') and e2.response:
                    second_error += f"\n响应状态: {e2.response.status_code}"
                    second_error += f"\n响应内容: {e2.response.text}"
                
                raise Exception(f"{error_msg}\n尝试替代格式也失败: {second_error}")