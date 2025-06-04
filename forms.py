from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    marca = StringField('Marca', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    preco = FloatField('Preço', validators=[DataRequired()])
    estoque = IntegerField('Estoque', validators=[DataRequired()])
    imagem = StringField('Imagem')
    submit = SubmitField('Salvar')

class OrderFilterForm(FlaskForm):
    status = SelectField('Status', choices=[('todos','Todos'), ('pendente','Pendente'), ('entregue','Entregue'), ('cancelado','Cancelado')])
    submit = SubmitField('Filtrar')

class AdminLoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')
