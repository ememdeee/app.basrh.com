from flask import Flask, render_template, request, url_for, send_from_directory, jsonify
from flask_cors import CORS
import idGrabber

app = Flask(__name__)
CORS(app, origins=["https://www.basrh.com"])

# declare home page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/id-grabber", methods = ["POST", "GET"])
def id_grabber():
    if request.method == "POST":
        try: 
            useOptionSelected = request.form["useOption"]
            # useCSV = request.form["useCSV"]
            links = request.form["links"]
            csv_file_input = request.files["csv"]
            # output, newFileName = idGrabber.main_function(links, csv_file_input, useOptionSelected)
            respond = idGrabber.main_function(links, csv_file_input, useOptionSelected)
            return jsonify(respond)
        except KeyError:
            return jsonify({"status": "Bad request. Some field is missing."})
    else:
        return render_template("id_grabber.html")

@app.route("/id-grabber/<filename>")
def idGrabber_download(filename):
    return send_from_directory ('output_csv', filename)


if __name__ == "__main__":
    app.run(debug=True)

application = app