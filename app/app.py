import bottle
import peewee
import uuid 

import mail


app = bottle.Bottle()
db = peewee.SqliteDatabase('user.db')
 
 
class User(peewee.Model):
    user = peewee.CharField(unique=True)
    pwd = peewee.CharField()
    email = peewee.CharField()
    activated = peewee.BooleanField()
 
    class Meta:
        database = db
 
class Token(peewee.Model):
    user = peewee.CharField()
    token = peewee.CharField()
 
    class Meta:
        database = db

db.connect()
db.create_tables([User, Token])
 
 
@app.post('/v1/user')
def user_add():
    """ Registro un Usuario Nuevo"""
    data = bottle.request.json
    msg = "Usuario Ingresado correctamente"
    try:
        token = str(uuid.uuid4())

        User(
            user=data["user"],
            pwd=data["pwd"],
            email=data["email"],
            activated=False
        ).save()

        Token(
            user = data["user"],
            token = token
        ).save()

        mail.enviar_mail(
            data["email"],
            token
        )

    except peewee.IntegrityError:
        msg = "El usuario ya existe"
 
    return msg
 

@app.get('/v1/activate/<token>')
def register_validate_token(token):
    """ Activate Account """
    data = Token(token=token).get()
    User.update({User.activated: True}).where(User.user == data.user)
    return "Account Activated"
    

@app.delete('/v1/user')
def user_delete():
    """ Borrar un usuario"""
    msg = "El Usuario ha sido borrado"
    data = bottle.request.json
    User.delete().where(User.user == data["user"]).execute()
 
    return msg
 
 
@app.put('/v1/user')
def user_update():
    """ Modificar un usuario """
    body = bottle.request.json
    User.update(**body).where(User.id == body["id"]).execute()
    return "ok"
 
 
@app.get('/v1/user')
def users():
    """ Listar todos los usuarios de la db """
    return "example"
 
 
app.run(host="0.0.0.0", port=5000)