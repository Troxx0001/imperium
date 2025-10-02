from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    FloatField,
    IntegerField,
    TextAreaField,
    SubmitField,
    SelectField,
    PasswordField,
    DateField,
)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


senha_policy = [
    Length(min=6, message="Mínimo de 6 caracteres."),
    Regexp(r".*[A-Z].*", message="Inclua pelo menos 1 letra maiúscula."),
    Regexp(r".*\d.*", message="Inclua pelo menos 1 número."),
]

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


class RegisterForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), *senha_policy])
    confirmar = PasswordField(
        "Confirmar senha", validators=[DataRequired(), EqualTo('senha')]
    )
    submit = SubmitField("Cadastrar")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Enviar link de recuperação")


class ResetPasswordForm(FlaskForm):
    senha = PasswordField("Nova senha", validators=[DataRequired(), *senha_policy])
    confirmar = PasswordField(
        "Confirmar senha", validators=[DataRequired(), EqualTo('senha')]
    )
    submit = SubmitField("Alterar senha")


class ChangePasswordForm(FlaskForm):
    atual = PasswordField("Senha atual", validators=[DataRequired()])
    nova = PasswordField("Nova senha", validators=[DataRequired(), *senha_policy])
    confirmar = PasswordField(
        "Confirmar nova senha", validators=[DataRequired(), EqualTo('nova')]
    )
    submit = SubmitField("Atualizar senha")
