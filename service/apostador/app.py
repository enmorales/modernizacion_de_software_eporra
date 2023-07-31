from . import create_app
import logging
from flask_restful import Api
from flask_cors import CORS
from .src.vistas import VistaApostador,  HelloWorld, VistaApostadores, VistaCheck, VistaCheckR
from .src.modelos import db

app = create_app("default")
logging.basicConfig(level=logging.DEBUG)
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
cors = CORS(app)


api = Api(app)
api.add_resource(HelloWorld,'/')
api.add_resource(VistaApostadores,'/api/apostadores')
api.add_resource(VistaApostador,'/api/apostador/<int:id_apostador>')
api.add_resource(VistaCheck,'/readiness_check')
api.add_resource(VistaCheckR,'/liveness_check')