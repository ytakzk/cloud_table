import argparse
from flask import Flask
import controller

def main():

    app = Flask(__name__)
    controller.init()

    parser = argparse.ArgumentParser(description='initial conditions')
    parser.add_argument('-port', action='store', default='9999', type=int)
    args = parser.parse_args()
    print(args)

    @app.route('/')
    def index():
        
        return '1'

    @app.route('/fetch_data/<int:index>')
    def fetch_data(index):
        
        return controller.fetch_data(index)

    @app.route('/manipulate/')
    def manipulate():
        
        return controller.manipulate()

    @app.route('/generate_mesh')
    def generate_mesh():

        return controller.generate_mesh()


    app.run(port=args.port, debug=True)

if __name__ == "__main__":
    
    main()