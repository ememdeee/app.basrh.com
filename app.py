from flask import Flask, render_template, request, url_for, send_from_directory, jsonify
from flask_cors import CORS
import idGrabber
import igLogin
import reupload

app = Flask(__name__)
# CORS(app, origins=["https://www.basrh.com"]) 
CORS(app)  # Allow Reqeust From All Source, good for testing
cl= None

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

@app.route('/reuploader', methods=['GET', 'POST'])
def reuploader():
    if request.method == 'POST':
        return "Received POST request"
    else:
        url = request.args.get('url')
        story = request.args.get('story')
        if url:
            reupload.reupload_function(cl, url, story)
            print("Application Stop Succesfuly.")
            return f"Content Uploaded"
        else:
            return render_template("igReuploader.html")

if __name__ == "__main__":
    cl=igLogin.login_function()
    app.run(debug=True)

application = app