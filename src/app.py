from flask_restful import Api

from setup import create_app
from api import ProcessEndpoint, SensorEndpoint


app = create_app()
api = Api(app)


api.add_resource(ProcessEndpoint, '/processes/', '/processes/<int:instance_id>')
api.add_resource(SensorEndpoint, '/sensors/', '/sensors/<int:instance_id>')

if __name__ == '__main__':
    app.run(debug=True)
