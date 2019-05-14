from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.events import NewRequest
from users import user_entry
from sqlalchemy import event
from logout import logout_entry
from login import login_entry
from flights import fly_entry
from reservations import reservation_entry

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)


if __name__ == '__main__':
    with Configurator() as config:
        config.add_subscriber(add_cors_headers_response_callback, NewRequest)
        config.set_authorization_policy(ACLAuthorizationPolicy())
        # Enable JWT authentication.
        config.include('pyramid_jwt')
        config.set_jwt_authentication_policy('secret')

        config.add_route('login', '/')  # localhost:6543/
        config.add_view(login_entry, route_name='login')
        config.add_route('users', '/users')
        config.add_view(user_entry, route_name='users')
        config.add_route('logout', '/logout')
        config.add_view(logout_entry, route_name='logout')
        config.add_route('flights', '/flights')
        config.add_view(fly_entry, route_name='flights')
        config.add_route('reservations', '/reservations')
        config.add_view(reservation_entry, route_name='reservations')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
