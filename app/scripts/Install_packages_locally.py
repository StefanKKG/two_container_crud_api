import sys
import subprocess

# implement pip as a subprocess:
def install_required_packages_locally():
    """
    This function automatically installs the required libraries
    that are needed in order to run this API application locally.
    """
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'flask'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'flask_restful'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                           'pandas'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                           'marshmallow'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                           'apispec'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                           'flask_swagger_ui'])
