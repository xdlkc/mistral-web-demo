import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename

from config import Config
from app.models.mistral_client import MistralClient
from app.models.chat_history import ChatHistory
from app.models.forms import TextChatForm, ImageChatForm

app = Flask(__name__)
app.config.from_object(Config)

# 创建上传目录
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 初始化组件
mistral_client = MistralClient()
chat_history = ChatHistory(app.config['HISTORY_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """首页显示聊天功能"""
    text_form = TextChatForm()
    image_form = ImageChatForm()
    
    # 获取或创建当前聊天会话ID
    chat_id = session.get('chat_id')
    if not chat_id:
        chat_id = chat_history.create_chat()
        session['chat_id'] = chat_id
    
    # 获取当前聊天的消息
    chat_data = chat_history.get_chat(chat_id)
    
    # 获取所有聊天历史
    all_chats = chat_history.get_all_chats()
    
    return render_template('index.html', 
                          text_form=text_form, 
                          image_form=image_form, 
                          chat=chat_data,
                          all_chats=all_chats)

@app.route('/chat/text', methods=['POST'])
def text_chat():
    """处理文本聊天"""
    form = TextChatForm()
    
    if form.validate_on_submit():
        message = form.message.data
        chat_id = session.get('chat_id')
        
        if not chat_id:
            chat_id = chat_history.create_chat()
            session['chat_id'] = chat_id
        
        # 保存用户消息
        chat_history.add_message(chat_id, 'user', message)
        
        # 获取聊天历史
        messages = chat_history.get_chat_messages(chat_id)
        
        # 调用Mistral API
        try:
            response = mistral_client.text_chat(messages)
            
            # 保存助手回复
            chat_history.add_message(chat_id, 'assistant', response)
            
            return jsonify({'status': 'success', 'response': response})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    return jsonify({'status': 'error', 'message': '表单验证失败'})

@app.route('/chat/image', methods=['POST'])
def image_chat():
    """处理图片聊天"""
    form = ImageChatForm()
    
    if form.validate_on_submit():
        message = form.message.data
        image = form.image.data
        
        chat_id = session.get('chat_id')
        if not chat_id:
            chat_id = chat_history.create_chat()
            session['chat_id'] = chat_id
        
        if image and allowed_file(image.filename):
            # 生成唯一文件名
            filename = secure_filename(image.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # 保存图片
            image.save(filepath)
            
            # 添加用户消息，包括图片信息
            user_message = f"[图片] {message}"
            chat_history.add_message(chat_id, 'user', user_message)
            
            # 获取聊天历史
            messages = chat_history.get_chat_messages(chat_id)
            
            # 调用Mistral API
            try:
                response = mistral_client.image_chat(messages, filepath)
                
                # 保存助手回复
                chat_history.add_message(chat_id, 'assistant', response)
                
                return jsonify({
                    'status': 'success', 
                    'response': response, 
                    'image_path': filepath.replace('\\', '/').replace(app.static_folder, '')
                })
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
    
    errors = {field: errors[0] for field, errors in form.errors.items()}
    return jsonify({'status': 'error', 'message': '表单验证失败', 'errors': errors})

@app.route('/chat/new', methods=['POST'])
def new_chat():
    """创建新的聊天会话"""
    chat_id = chat_history.create_chat()
    session['chat_id'] = chat_id
    return redirect(url_for('index'))

@app.route('/chat/load/<chat_id>', methods=['GET'])
def load_chat(chat_id):
    """加载指定的聊天会话"""
    chat_data = chat_history.get_chat(chat_id)
    if chat_data:
        session['chat_id'] = chat_id
        return redirect(url_for('index'))
    flash('找不到聊天会话')
    return redirect(url_for('index'))

@app.route('/chat/delete/<chat_id>', methods=['POST'])
def delete_chat(chat_id):
    """删除聊天会话"""
    current_chat_id = session.get('chat_id')
    if chat_history.delete_chat(chat_id):
        if current_chat_id == chat_id:
            # 如果删除的是当前会话，创建新会话
            new_chat_id = chat_history.create_chat()
            session['chat_id'] = new_chat_id
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': '删除失败'})

if __name__ == '__main__':
    app.run(debug=True)
