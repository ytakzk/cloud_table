import argparse
from flask import Flask, request, jsonify, render_template
import webapp_controller as controller

def main():

    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    controller.init()

    @app.route('/')
    def index():
        
        return render_template('index.html')

    @app.route('/semantic_morphing')
    def semantic_morphing():
        
        return render_template('semantic_morphing.html')

    @app.route('/weather_table')
    def weather_table():
        
        return render_template('weather_table.html')

    @app.route('/create_weather_table/<int:time_index>')
    def create_weather_table(time_index):
        
        res = controller.create_weather_table(time_index)
        return jsonify(point_clouds=res[0], places=res[1], weathers=res[2])


    @app.route('/fetch_point_clouds/<int:index>')
    def fetch_point_clouds(index):
        
        return jsonify(point_clouds=controller.fetch_point_clouds(index))

    @app.route('/manipulate', methods=['POST'])
    def manipulate():

        data = request.json
        point_clouds = controller.manipulate(data)
        return jsonify(point_clouds=point_clouds)

    @app.route('/generate_mesh', methods=['POST'])
    def generate_mesh():

        data = request.json
        mesh = controller.generate_mesh(data)
        return mesh

    app.run(host='0.0.0.0', port=9997, debug=True)

if __name__ == "__main__":

    main()
