from flask import Flask, render_template, request, url_for, send_from_directory
import idGrabber

app = Flask(__name__)

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
        useOptionSelected = request.form["useOption"]
        # useCSV = request.form["useCSV"]
        links = request.form["links"]
        csv_file_input = request.files["csv"]
        output, newFileName = idGrabber.main_function(links, csv_file_input, useOptionSelected)
        # run python function from other file
        return f"<p id='links' class='output links'>Link: {links}</p><p id='csv' class='output csv'>CSV: {csv_file_input.filename}</p><p id='option' class='output option'>Option: {useOptionSelected}</p><p id='outputValue' class='output outputValue'>Output: {output}</p><p id='download' class='output download'>Download: <a href='{url_for('idGrabber_download', filename=newFileName)}'>{newFileName}</a></p>"
    else:
        return render_template("id_grabber.html")

@app.route("/id-grabber/<filename>")
def idGrabber_download(filename):
    return send_from_directory ('output_csv', filename)


if __name__ == "__main__":
    app.run(debug=True)