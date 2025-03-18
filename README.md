# Mistral AI 聊天应用

一个基于Flask的Web应用程序，允许用户通过文字或图片与Mistral AI模型进行对话。

## 功能特性

- 💬 纯文本对话 - 向Mistral AI发送文字提问并获取回答
- 🖼️ 图片对话 - 上传图片并提问，Mistral AI将分析图片内容
- 📝 连续对话 - 支持上下文连续对话，Mistral AI能理解之前的对话内容
- 📜 历史记录 - 自动保存聊天历史，并支持查看、切换、删除历史会话
- 🎨 美观界面 - 现代化设计的用户界面，支持响应式布局

## 技术栈

- **后端**: Flask, Python
- **前端**: HTML, CSS, JavaScript, Bootstrap 5
- **AI**: Mistral AI API
- **存储**: 本地文件系统存储

## 安装步骤

1. 克隆仓库:
   ```
   git clone <repo-url>
   cd mistral-app
   ```

2. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

3. 设置环境变量:
   创建一个 `.env` 文件并添加以下内容:
   ```
   MISTRAL_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

4. 运行应用:
   ```
   python app.py
   ```

5. 在浏览器中访问:
   ```
   http://127.0.0.1:5000
   ```

## 使用说明

1. **文本对话**: 点击"文本对话"按钮，在输入框中输入问题并发送。
2. **图片对话**: 点击"图片对话"按钮，选择图片并输入关于图片的问题。
3. **新建对话**: 点击左侧边栏中的"新聊天"按钮创建新的对话。
4. **查看历史**: 在左侧边栏中可以看到所有聊天历史，点击任一历史可以继续对话。
5. **删除历史**: 点击聊天历史条目右侧的删除图标可以删除该对话历史。

## 项目结构

```
mistral-app/
│
├── app/                    # 应用模块
│   └── models/             # 模型定义
│       ├── mistral_client.py  # Mistral API 客户端
│       ├── chat_history.py    # 聊天历史管理
│       └── forms.py           # 表单定义
│
├── static/                 # 静态资源
│   ├── css/                # 样式文件
│   ├── js/                 # JavaScript文件
│   └── uploads/            # 上传的图片
│
├── templates/              # HTML模板
│   ├── base.html           # 基础模板
│   └── index.html          # 首页模板
│
├── chat_history/           # 聊天历史存储目录
├── app.py                  # 应用主文件
├── config.py               # 配置文件
└── requirements.txt        # 依赖列表
```

## 注意事项

- 此应用需要有效的Mistral AI API密钥才能运行
- 上传的图片和聊天历史存储在本地，请确保有足够的磁盘空间
- 默认情况下，应用运行在开发模式，不建议在生产环境中直接使用

## 许可证

[MIT](LICENSE) 