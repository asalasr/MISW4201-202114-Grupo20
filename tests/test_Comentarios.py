import unittest
import json
from flaskr.app import app
from flaskr.modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema, Compartida_cancion, Compartida_album, AlbumComentario
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

class test_Compartir(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        nuevo_usuario = Usuario(nombre="ELadminTest", contrasena="xxx7632xxa3199930")
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        self.userId = nuevo_usuario.id
        self.userName = "ELadminTest"

        token_de_acceso = create_access_token(identity = nuevo_usuario.id)
        self.token = token_de_acceso
        nuevo_Album = Album(titulo="titulo8885446", anio=2021, descripcion="interprete88879993dc222", medio="CD")
        db.session.add(nuevo_Album)
        self.nuevo_Album = nuevo_Album
        db.session.commit()
        self.albumId = nuevo_Album.id
        self.message = "el mensaje de text"

        

    def test_CrearComentario(self):
        payload = json.dumps(
            {
                "id_album":self.albumId,
                "message":self.message

            }
        )

        response = self.app.post('/album/comentarios', headers={"Content-Type": "application/json",'Authorization': 'Bearer '+ self.token}, data=payload)
        
        self.assertEqual(202, response.status_code)
        self.assertEqual("successes", response.json['mensaje'])
        
        comentarios = AlbumComentario.query.filter( AlbumComentario.id_album==self.albumId).all()
        if comentarios is None:
            self.assertEqual(1, 0)
        else:
            for com in comentarios:
                if self.message == com.comentario:
                   self.assertEqual(1, 1) 
                else:
                   self.assertEqual(1, 0) 
                
            db.session.delete(com)
            db.session.commit()


    def test_TraerComentarios(self):
        nueva_comentario = AlbumComentario(comentario = self.message, id_album=self.albumId, usuario=self.userId)
        db.session.add(nueva_comentario)
        db.session.commit()

        response = self.app.get('/album/'+str(self.albumId)+'/comentarios', headers={"Content-Type": "application/json",'Authorization': 'Bearer '+ self.token})
        
        self.assertEqual(202, response.status_code)
        self.assertEqual(1, len(response.json['comments']))

        comentarios = AlbumComentario.query.filter( AlbumComentario.id_album==self.albumId).all()
        if comentarios is None:
            self.assertEqual(1, 0)
        else:
            for com in comentarios:
                if self.message == com.comentario:
                   self.assertEqual(1, 1) 
                else:
                   self.assertEqual(1, 0) 
                
            db.session.delete(com)
            db.session.commit()
    
    def tearDown(self):
        
        db.session.delete(self.nuevo_Album)
        db.session.commit()
        
        user = Usuario.query.get_or_404(self.userId)
        db.session.delete(user)
        db.session.commit()
        