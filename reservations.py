from pyramid.response import Response
from sqlalchemy.sql.elements import TextClause
from sqlalchemy import text
from database import db


def reservation_entry(request):
    if request.method == 'OPTIONS':
        return Response(status=200)
    if request.method == 'POST':
        return create_reservation(request)

def create_reservation(request):
    reservation = request.json_body
    #stmt: TextClause = text('INSERT ')
