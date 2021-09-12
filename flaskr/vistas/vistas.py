from flask import request
from ..modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema, Compartida_cancion, Compartida_album, CompartirAlbumSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import sys

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
album_schema = AlbumSchema()
compartir_album_schema = CompartirAlbumSchema()


class VistaCanciones(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.canciones.append(nueva_cancion)
        try:
            db.session.commit()
            return {"mensaje":"cancion creada exitosamente"}
        except IntegrityError:
            db.session.rollback()
            return 'Error de creacion de cancion',409

    
    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        
        cancionesCompartidos = []
        
        compartida = Compartida_cancion.query.filter( Compartida_cancion.usuario_id==id_usuario).all()
        if compartida is None:
            return {"mensaje":"successes", "compartidas": cancionesCompartidos, "propios":[cancion_schema.dump(ca) for ca in usuario.canciones]},202
        else:
            
            for com in compartida:
                cancionesCompartidos.append(cancion_schema.dump(Cancion.query.get_or_404(com.cancion_id)))
            return {"mensaje":"successes", "compartidas": cancionesCompartidos, "propios":[cancion_schema.dump(ca) for ca in usuario.canciones]},202 

class VistaCancion(Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))

    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get("titulo",cancion.titulo)
        cancion.minutos = request.json.get("minutos",cancion.minutos)
        cancion.segundos = request.json.get("segundos",cancion.segundos)
        cancion.interprete = request.json.get("interprete",cancion.interprete)
        cancion.usuario = request.json.get("usuario",cancion.usuario)
        db.session.commit()
        return cancion_schema.dump(cancion)

    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return '',204

class VistaAlbumesCanciones(Resource):
    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        return [album_schema.dump(al) for al in cancion.albumes]
        

class VistaSignIn(Resource):
    
    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity = nuevo_usuario.id)
        return {"mensaje":"usuario creado exitosamente", "token":token_de_acceso}


    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204

class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}


class VistaAlbumsUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre',409

        return album_schema.dump(nuevo_album)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        
        albumesCompartidos = []
        
        compartida = Compartida_album.query.filter( Compartida_album.usuario_id==id_usuario).all()
        if compartida is None:
            return {"mensaje":"successes", "compartidas": albumesCompartidos, "propios":[album_schema.dump(al) for al in usuario.albumes]},202
        else:
            
            for com in compartida:
                albumesCompartidos.append(album_schema.dump(Album.query.get_or_404(com.album_id)))
            return {"mensaje":"successes", "compartidas": albumesCompartidos, "propios":[album_schema.dump(al) for al in usuario.albumes]},202 
        

class VistaCancionesAlbum(Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)
        
        if "id_cancion" in request.json.keys():
            
            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea',404
        else: 
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)
       
    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]

class VistaAlbum(Resource):

    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))

    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get("titulo",album.titulo)
        album.anio = request.json.get("anio", album.anio)
        album.descripcion = request.json.get("descripcion", album.descripcion)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)

    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '',204

class VistaUsuarioData(Resource):
    @jwt_required()
    def get(self, id_usuario):
        return usuario_schema.dump(Usuario.query.get_or_404(id_usuario))

class VistaUsuario(Resource):
    
    def post(self):
        arrayUsuarios = request.json["lista"]
        usuarioNoExist = []
        for user in arrayUsuarios:
            usuario = Usuario.query.filter(Usuario.nombre == user).first()
            if usuario is None:
                usuarioNoExist.append(user)
        db.session.commit()
        
        if usuarioNoExist != []:
            return {"mensaje":"Error","listaNoExiste":usuarioNoExist}, 404
        else:
            return {"mensaje":"successes"},202
    

class VistaCompartirCancion(Resource):
 
    def post(self):
        id_cancion = request.json["id_cancion"]
        arrayUsuarios = request.json["lista_usuarios"]
        arrayUsuariosId = []
        usuarioNoExist = []
        for user in arrayUsuarios:
            usuario = Usuario.query.filter(Usuario.nombre == user).first()
            if usuario is None:
                usuarioNoExist.append(user)
            else:
                arrayUsuariosId.append(usuario)

        if usuarioNoExist != []:
            return {"mensaje":"Error","listaNoExiste":usuarioNoExist}, 404
        else:
             for user in arrayUsuariosId:
                try:
                    compartida = Compartida_cancion.query.filter(Compartida_cancion.cancion_id==id_cancion, Compartida_cancion.usuario_id==user.id).first()
                    
                    if compartida is None:
                       
                        nueva_compartida = Compartida_cancion(cancion_id=id_cancion, usuario_id=user.id)
                        db.session.add(nueva_compartida)
                        db.session.commit()
                   
                except:
                    print("Repetida, ignorar")

        return {"mensaje":"successes"},202

class VistaCompartirAlbum(Resource):
     
    def post(self):
        id_album = request.json["id_album"]
        arrayUsuarios = request.json["lista_usuarios"]
        arrayUsuariosId = []
        usuarioNoExist = []
        for user in arrayUsuarios:
            usuario = Usuario.query.filter(Usuario.nombre == user).first()
            if usuario is None:
                usuarioNoExist.append(user)
            else:
                arrayUsuariosId.append(usuario)

        if usuarioNoExist != []:
            return {"mensaje":"Error usuario no existe","listaNoExiste":usuarioNoExist}, 404
        else:
             for user in arrayUsuariosId:
                try:
                   
                    compartida = Compartida_album.query.filter(Compartida_album.album_id==id_album, Compartida_album.usuario_id==user.id).first()
                    if compartida is None:
                       
                        nueva_compartida = Compartida_album(album_id=id_album, usuario_id=user.id)
                        db.session.add(nueva_compartida)
                        db.session.commit()
                        
                    
                except Exception:
                    e = sys.exc_info()[1]
                    print(e.args[0])
                    return {"mensaje":"Error", "error":e.args[0]}, 404

        return {"mensaje":"successes"},202     



                    
                    
           