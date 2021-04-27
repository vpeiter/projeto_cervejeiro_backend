from flask_restful import Api

from setup import create_app
from api import ProcessEndpoint, ProcessListEndpoint


app = create_app()
api = Api(app)

api.add_resource(ProcessListEndpoint, '/processes')
api.add_resource(ProcessEndpoint, '/processes/<int:instance_id>')

if __name__ == '__main__':
    app.run(debug=True)
