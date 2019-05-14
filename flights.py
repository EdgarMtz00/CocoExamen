from pyramid.response import Response
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause
from sqlalchemy import text
from database import db
import json


def fly_entry(request):
    if request.method == 'OPTIONS':
        return Response(status=200)
    if request.method == 'GET':
        return get_fly(request)
    if request.method == 'POST':
        return create_reservation(request)


def create_reservation(request):
    try:
        data = request.json_body
        user = request.authenticated_userid
        stmt: TextClause = text(
            'INSERT into reservaciones (usuario, vuelo, cantidad) VALUES (:user, :flight, :quantity)')
        stmt = stmt.bindparams(user=user, flight=data['id'], quantity=data['quantity'])
        db.execute(stmt)
        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=500)


def get_fly(request):
    origin = request.params.get('origin', -1)
    destination = request.params.get('destination', -1)
    if origin != -1 and destination != -1:
        stmt: TextClause = text("Select * from vuelo where destino = :destino and  origen = :origen")
        stmt = stmt.bindparams(destino=destination, origen=origin)
        result: ResultProxy = db.execute(stmt)
        result = [dict(r) for r in result]
    else:
        stmt: TextClause = text("Select * from vuelo")
        result: ResultProxy = db.execute(stmt)
        result = [dict(r) for r in result]
    return Response(status=200, content_type='application/json',
                    body=json.dumps(result),
                    charset='utf-8')
