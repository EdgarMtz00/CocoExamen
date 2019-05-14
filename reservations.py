from pyramid.response import Response
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause
from sqlalchemy import text
from database import db
import json

def reservation_entry(request):
    if request.method == 'OPTIONS':
        return Response(status=200)
    if request.method == 'GET':
        return get_reservation(request)


def get_reservation(request):
    try:
        users = request.authenticated_userid
        stmt: TextClause = text(
            'Select * from reservaciones as r inner join vuelo as v on r.vuelo = v.pk_vuelo where r.usuario  = :usr')
        stmt = stmt.bindparams(usr=users)
        result: ResultProxy = db.execute(stmt)
        result = [dict(r) for r in result]
        return Response(status=200, content_type='application/json',
                                body=json.dumps(result),
                                charset='utf-8')
    except Exception as e:
        print(e)
        return Response(status=404)
