# The below library enables the logic for the CRUD functionality of our APIs. 
from flask_restful import Resource


class API_Status_Check(Resource):
    """
    This class returns a success message if the API is up and running.
    """

    def get(self):
        return {"200": "If you see this message then that means that the containerized CRUD API is up and running."}

