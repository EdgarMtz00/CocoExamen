from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause

from database import db
import json


def login_entry(request):
    if request.method == 'OPTIONS':
        return login_cors(request)
    user = request.json_body['user']
    pwd = request.json_body['password']
    try:
        stmt: TextClause = text('SELECT "pk_usuario", "conexion" from usuario '
                                'where usuario."usuario" = :user AND "contraseña" = :pwd')
        stmt = stmt.bindparams(user=user, pwd=pwd)
        result: ResultProxy = db.execute(stmt)
        user_id = [dict(r) for r in result][0]
        print(user_id)
        if user_id is not None and not user_id['conexion']:
            token = request.create_jwt_token(user_id['pk_usuario'])
            stmt: TextClause = text('UPDATE usuario SET conexion = true where pk_usuario = :id')
            stmt = stmt.bindparams(id=user_id['pk_usuario'])
            db.execute(stmt)
            return Response(status=200, content_type='application/json',
                            body=json.dumps({'token': token}),
                            charset='utf-8')
    except Exception as e:
        print(e)
        return Response(status=404, content_type='application/json')
    return Response(status=404, content_type='application/json')


@view_config(request_method='OPTIONS')
def login_cors(request):
    return Response(status=200)
