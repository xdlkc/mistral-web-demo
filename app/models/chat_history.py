import os
import json
import uuid
from datetime import datetime

class ChatHistory:
    def __init__(self, history_folder):
        self.history_folder = history_folder
        if not os.path.exists(history_folder):
            os.makedirs(history_folder, exist_ok=True)
    
    def create_chat(self):
        """创建新的聊天会话"""
        chat_id = str(uuid.uuid4())
        chat_data = {
            'id': chat_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'messages': []
        }
        
        self._save_chat(chat_id, chat_data)
        return chat_id
    
    def add_message(self, chat_id, role, content):
        """添加一条消息到聊天历史"""
        chat_data = self._load_chat(chat_id)
        
        if chat_data:
            chat_data['messages'].append({
                'role': role,
                'content': content,
                'timestamp': datetime.now().isoformat()
            })
            chat_data['updated_at'] = datetime.now().isoformat()
            self._save_chat(chat_id, chat_data)
            return True
        return False
    
    def get_chat(self, chat_id):
        """获取一个聊天会话的所有内容"""
        return self._load_chat(chat_id)
    
    def get_all_chats(self):
        """获取所有聊天会话的摘要"""
        chats = []
        if os.path.exists(self.history_folder):
            for filename in os.listdir(self.history_folder):
                if filename.endswith('.json'):
                    chat_id = filename.replace('.json', '')
                    chat_data = self._load_chat(chat_id)
                    if chat_data:
                        # 只包含摘要信息
                        chats.append({
                            'id': chat_data['id'],
                            'created_at': chat_data['created_at'],
                            'updated_at': chat_data['updated_at'],
                            'message_count': len(chat_data['messages']),
                            'preview': chat_data['messages'][0]['content'][:50] + '...' if chat_data['messages'] else ''
                        })
        # 按照更新时间排序，最新的在前面
        chats.sort(key=lambda x: x['updated_at'], reverse=True)
        return chats
    
    def delete_chat(self, chat_id):
        """删除一个聊天会话"""
        filepath = os.path.join(self.history_folder, f"{chat_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    def _save_chat(self, chat_id, chat_data):
        """保存聊天数据到文件"""
        filepath = os.path.join(self.history_folder, f"{chat_id}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, ensure_ascii=False, indent=2)
    
    def _load_chat(self, chat_id):
        """从文件加载聊天数据"""
        filepath = os.path.join(self.history_folder, f"{chat_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return None
        return None
    
    def get_chat_messages(self, chat_id):
        """获取聊天会话的所有消息，格式适合Mistral API使用"""
        chat_data = self._load_chat(chat_id)
        if chat_data and 'messages' in chat_data:
            # 转换为Mistral API需要的格式
            return [{'role': msg['role'], 'content': msg['content']} for msg in chat_data['messages']]
        return [] 