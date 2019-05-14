from pyramid.response import Response
from sqlalchemy.sql.elements import TextClause

from sqlalchemy import text
from database import db


def logout(request):
    try:
        user_id = request.authenticated_userid
        stmt: TextClause = text('UPDATE usuario SET conexion = false where pk_usuario = :id')
        stmt = stmt.bindparams(id=user_id)
        db.execute(stmt)
        return Response(status=200)
    except Exception as e:
        print(e)


def logout_entry(request):
    if request.method == 'OPTIONS':
        return Response(status=200)
    if request.method == 'POST':
        return logout(request)
