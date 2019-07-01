from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


# OpenID 登录仅仅需要一个字符串，被称为 OpenID。我们将在表单上提供一个 ‘remember me’ 的选择框，以至于用户可以选择在他们的网页浏览器上种植 cookie ，当他们再次访问的时候，浏览器能够记住他们的登录。
# datarequired验证器只检测提交数据是否为空
class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
