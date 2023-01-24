# The below library imports the main Flask functionalitiers that we need to build this app.
from flask import Flask
# The below library is used to turn out Flask app into a Flask API app.
from flask_restful import Api
# The below library is used to create the API documentation.
from flask_swagger_ui import get_swaggerui_blueprint

# Below I am importing all of my own defined functions and classes.
from app.sql.SQL_functions import create_table_if_not_exists
from app.sql.SQL_functions import load_data_only_once_from_csv_into_db
from app.routes.API import API_Status_Check
from app.routes.person import CREATE_and_read_all_people
from app.routes.person import GET_UPDATE_DELETE_person

#If you are getting error about missing libraries while testing this app locally, run the function: 'install_required_packages_locally()
from app.scripts.Install_packages_locally import install_required_packages_locally

# Declare global variables
app = Flask(__name__)
api = Api(app)

# Define the API endpoint that we can access to view the API documentation in the browser.
SWAGGER_URL = "/openapidocs"

# Define the path to the OpenAPI specification which is visualized in the browser at the endpoint '/openapidocs'.
# The flask-swagger-ui library requires that the .yaml file with the OpenAPI specification be located in a folder called 'static'.
# If we put the OpenAPI specification in another folder, then the OpenAPI spec will not be visualized in the browser.
# See: https://stackoverflow.com/questions/55733136/flask-swagger-ui-does-not-recognize-path-to-swagger-json

#URL I SHOULD USE
API_URL = "/static/openapi.yaml"


# Define the blueprint of the OpenAPI specification that is displayed in the brower.
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "CRUD API"
    }
)

# Add the CRUD functionalities and their specified context paths to the API.
api.add_resource(API_Status_Check, "/api")
api.add_resource(CREATE_and_read_all_people, "/api/v1/person")
api.add_resource(GET_UPDATE_DELETE_person, "/api/v1/person/<int:row_id>")

# Connect or register the OpenAPI specification with and to the API application so that the OpenAPI specification can be viewed and accessed.
app.register_blueprint(swaggerui_blueprint)
 
# Define the main logic of the application.
if __name__ == "__main__":
    print ("*************************************************************************")
    print ("ACCESS THE OPENAPI DOCUMENTATION HERE: http://127.0.0.1:5001/openapidocs")
    print("*************************************************************************")
    create_table_if_not_exists()
    load_data_only_once_from_csv_into_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
