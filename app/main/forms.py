from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField 
from wtforms import BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField
from ..models import Role, User

class BaseForm(Form):
	LANGUAGES = ['zh']
		
class NameForm(BaseForm):
	name = StringField(u"你的名字：", validators=[Required()])
	submit = SubmitField(u"提交")

class EditProfileForm(BaseForm):
	name = StringField(u'真实姓名', validators=[Length(0, 64)])
	location = StringField(u'现居地', validators=[Length(0, 64)])
	about_me = TextAreaField(u'关于我')
	submit = SubmitField(u'提交')

class EditProfileAdminForm(BaseForm):
	email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
		Email()])
	username = StringField(u'用户名', validators=[Required(), 
		Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
			u'用户名只能由字母、数字、下划线、点号组成。')])
	confirmed = BooleanField(u'验证')
	role = SelectField(u'角色', coerce=int)
	name = StringField(u'真实姓名', validators=[Length(0, 64)])
	location = StringField(u'现居地', validators=[Length(0, 64)])
	about_me = TextAreaField(u'关于我')
	submit = SubmitField(u'提交')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and \
		User.query.filter_by(email=field.data).first():
			raise ValidationError(u'该邮箱已被注册。')

	def validate_username(self, field):
		if field.data != self.username and \
		User.query.filter_by(username=field.data).first():
			raise ValidationError(u'用户名已存在。')

class PostForm(BaseForm):
	body = PageDownField(u"说点儿什么？", validators=[Required()])
	submit = SubmitField(u'提交')

class CommentForm(BaseForm):
	body = PageDownField('', validators=[Required()])
	submit = SubmitField(u'提交评论')