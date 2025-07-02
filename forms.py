from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SubmitField, SelectField, PasswordField, DateField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    marca = StringField('Marca', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    preco = FloatField('Preço', validators=[DataRequired()])
    estoque = IntegerField('Estoque', validators=[DataRequired()])
    imagem_url = StringField('URL da imagem')
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Salvar')

class OrderFilterForm(FlaskForm):
    status = SelectField('Status', choices=[('todos','Todos'), ('pendente','Pendente'), ('entregue','Entregue'), ('cancelado','Cancelado')])
    cliente = StringField('Cliente')
    data_inicio = DateField('De', format='%Y-%m-%d')
    data_fim = DateField('Até', format='%Y-%m-%d')
    submit = SubmitField('Filtrar')

class AdminLoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')
