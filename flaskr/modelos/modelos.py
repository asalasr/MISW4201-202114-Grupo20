from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum
import datetime

db = SQLAlchemy()

albumes_canciones = db.Table('album_cancion',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True),
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key = True))



class Compartida_cancion(db.Model):
    cancion_id = db.Column( db.Integer, db.ForeignKey('cancion.id'), primary_key = True)
    usuario_id = db.Column( db.Integer, db.ForeignKey('usuario.id'), primary_key = True)

class Compartida_album(db.Model):
    album_id = db.Column( db.Integer, db.ForeignKey('cancion.id'), primary_key = True)
    usuario_id = db.Column( db.Integer, db.ForeignKey('usuario.id'), primary_key = True)

class Cancion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    minutos = db.Column(db.Integer)
    segundos = db.Column(db.Integer)
    interprete = db.Column(db.String(128))
    albumes = db.relationship('Album', secondary = 'album_cancion', back_populates="canciones")
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))

class Medio(enum.Enum):
   DISCO = 1
   CASETE = 2
   CD = 3

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128))
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.String(512))
    medio = db.Column(db.Enum(Medio))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    canciones = db.relationship('Cancion', secondary = 'album_cancion', back_populates="albumes")
    comentarios = db.relationship('AlbumComentario', cascade='all, delete, delete-orphan')
    
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    albumes = db.relationship('Album', cascade='all, delete, delete-orphan')
    canciones = db.relationship('Cancion', cascade='all, delete, delete-orphan')
    comentarios = db.relationship('AlbumComentario', cascade='all, delete, delete-orphan')

class AlbumComentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(50))
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    id_album = db.Column(db.Integer, db.ForeignKey("album.id"))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    
class CancionComentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(50))
    fecha = db.Column(db.DateTime, default=datetime.datetime.now)
    id_cancion = db.Column(db.Integer, db.ForeignKey("cancion.id"))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class CancionSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Cancion
         include_relationships = True
         load_instance = True

class AlbumSchema(SQLAlchemyAutoSchema):
    medio = EnumADiccionario(attribute=("medio"))
    class Meta:
         model = Album
         include_relationships = True
         load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True

class CompartirAlbumSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Compartida_album
         include_relationships = True
         load_instance = True

