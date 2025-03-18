from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TextChatForm(FlaskForm):
    """纯文本聊天表单"""
    message = StringField('消息', validators=[DataRequired(message='请输入消息')])
    submit = SubmitField('发送')

class ImageChatForm(FlaskForm):
    """图片聊天表单"""
    message = StringField('消息', validators=[DataRequired(message='请输入关于图片的问题')])
    image = FileField('图片', validators=[
        DataRequired(message='请选择图片'),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='仅支持jpg, jpeg, png, gif格式')
    ])
    submit = SubmitField('发送') 