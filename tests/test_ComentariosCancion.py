import unittest
import json
from flaskr.app import app
from flaskr.modelos import db,  Usuario, CancionComentario, Cancion
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

class test_ComentarioCancion(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        nuevo_usuario = Usuario(nombre="ELadminTest", contrasena="xxx7632xxa3199930")
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        self.userId = nuevo_usuario.id
        self.userName = "ELadminTest"

        token_de_acceso = create_access_token(identity = nuevo_usuario.id)
        self.token = token_de_acceso
        nuevo_Cancion = Cancion(titulo="titulo8885446", minutos=3, segundos=3, interprete="interprete8887999",usuario=self.userId)
        db.session.add(nuevo_Cancion)
        self.nuevo_Cancion = nuevo_Cancion
        db.session.commit()
        self.cancionId = nuevo_Cancion.id
        self.message = "el mensaje de text"

        

    def test_CrearComentario(self):
        payload = json.dumps(
            {
                "id_cancion":self.cancionId,
                "message":self.message

            }
        )

        response = self.app.post('/cancion/comentarios', headers={"Content-Type": "application/json",'Authorization': 'Bearer '+ self.token}, data=payload)
        
        self.assertEqual(202, response.status_code)
        self.assertEqual("successes", response.json['mensaje'])
        
        comentarios = CancionComentario.query.filter( CancionComentario.id_cancion==self.cancionId).all()
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
        nueva_comentario = CancionComentario(comentario = self.message, id_cancion=self.cancionId, usuario=self.userId)
        db.session.add(nueva_comentario)
        db.session.commit()

        response = self.app.get('/cancion/'+str(self.cancionId)+'/comentarios', headers={"Content-Type": "application/json",'Authorization': 'Bearer '+ self.token})
        
        self.assertEqual(202, response.status_code)
        self.assertEqual(1, len(response.json['comments']))

        comentarios = CancionComentario.query.filter( CancionComentario.id_cancion==self.cancionId).all()
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
        
        db.session.delete(self.nuevo_Cancion)
        db.session.commit()
        
        user = Usuario.query.get_or_404(self.userId)
        db.session.delete(user)
        db.session.commit()
        