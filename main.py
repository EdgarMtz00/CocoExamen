from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy

if __name__ == '__main__':
    with Configurator() as config:
        config.set_authorization_policy(ACLAuthorizationPolicy())
        # Enable JWT authentication.
        config.include('pyramid_jwt')
        config.set_jwt_authentication_policy('secret')

        config.add_route('root', '/')  # localhost:6543/
        # config.add_view(, route_name='root')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
