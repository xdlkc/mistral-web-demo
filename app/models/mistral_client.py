import os
import base64
from mistralai import Mistral

class MistralClient:
    def __init__(self):
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY 环境变量未设置")
        self.model = "mistral-small-latest"  # 支持视觉功能
        self.client = Mistral(api_key=self.api_key)
    
    def text_chat(self, messages):
        """处理纯文本对话"""
        # 转换消息格式为原生字典
        chat_messages = []
        for msg in messages:
            chat_messages.append({
                "role": msg["role"], 
                "content": msg["content"]
            })
        
        # 使用官方推荐的client.chat.complete方法
        response = self.client.chat.complete(
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
        chat_messages = []
        
        # 添加历史消息
        for i, msg in enumerate(messages):
            if i < len(messages) - 1:  # 不是最后一条消息
                chat_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # 添加带图像的最后一条消息
        last_msg = messages[-1]
        chat_messages.append({
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
        
        try:
            # 使用官方推荐的client.chat.complete方法
            response = self.client.chat.complete(
                model=self.model,
                messages=chat_messages
            )
            return response.choices[0].message.content
        except Exception as e:
            try:
                # 如果出错，尝试使用另一种格式
                chat_messages[-1]["content"][-1]["image_url"] = {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                response = self.client.chat.complete(
                    model=self.model,
                    messages=chat_messages
                )
                return response.choices[0].message.content
            except Exception as e2:
                # 记录详细错误信息
                error_msg = f"图像处理失败: {str(e)}"
                second_error = f"{str(e2)}"
                raise Exception(f"{error_msg}\n尝试替代格式也失败: {second_error}")