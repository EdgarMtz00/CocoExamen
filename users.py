from pyramid.response import Response

from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause

from database import db
import json


def create_user(request):
    try:
        user_data = request.json_body
        stmt: TextClause = text('INSERT Into usuario (usuario, contraseña, conexion) values (:user, :pwd, true) returning pk_usuario')
        stmt = stmt.bindparams(user=user_data['user'], pwd=user_data['password'])
        result: ResultProxy = db.execute(stmt)
        result = [dict(r) for r in result][0]
        if result is not None:
            token = request.create_jwt_token(result['pk_usuario'])
            return Response(status=200, content_type='application/json',
                            body=json.dumps({'token': token}),
                            charset='utf-8')
    except Exception as e:
        print(e)
        return Response(status=404, content_type='application/json')
    return Response(status=404, content_type='application/json')


def user_entry(request):
    if request.method == 'OPTIONS':
        return Response(status=200)
    if request.method == 'POST':
        return create_user(request)
