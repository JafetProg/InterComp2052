from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)
app.config["SECRET_KEY"] = "mi_clave_secreta"

class RegisterForm(FlaskForm):
    nombre = StringField("Nombre", validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, message="El nombre debe tener al menos 3 caracteres.")
    ], render_kw={"placeholder": "Tu nombre"})

    correo = EmailField("Correo electrónico", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Debes ingresar un correo válido.")
    ], render_kw={"placeholder": "tucorreo@ejemplo.com"})

    contrasena = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
    ], render_kw={"placeholder": "Tu contraseña"})

    submit = SubmitField("Registrar", render_kw={"class": "btn btn-primary"})


@app.route("/", methods=["GET", "POST"])
def index():
    form = RegisterForm()
    if form.validate_on_submit():
        message = f"Usuario registrado: {form.nombre.data} ({form.correo.data})"
        return render_template("home.html", message=message)
    return render_template("index.html.jinja2", form=form)


if __name__ == "__main__":
    app.run(debug=True)
