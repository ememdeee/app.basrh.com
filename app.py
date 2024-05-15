from flask import Flask, render_template, request, url_for, send_from_directory, jsonify
from flask_cors import CORS
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import idGrabber
import igLogin
import reupload
from urls import URLS, URLS2

app = Flask(__name__)
# CORS(app, origins=["https://www.basrh.com"]) 
CORS(app)  # Allow Reqeust From All Source, good for testing
schedulerFeedStory = BackgroundScheduler()
schedulerStory = BackgroundScheduler()
schedulerFeedStory2 = BackgroundScheduler()
schedulerStory2 = BackgroundScheduler()
feedStoryList = URLS
feedStoryList2 = URLS2
cl= None
cl2= None
userName="default"
userName2="default2"

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
        acc = request.args.get('acc')
        if url:
            if acc == "1":
                reupload.reupload_function(cl, userName, url, story)
            elif acc == "2":
                reupload.reupload_function(cl2, userName2, url, story)
            else:
                print ("acc query string not available or not valid, upload using default acc.")
                reupload.reupload_function(cl, userName, url, story)
            print("Application Stop Succesfuly.")
            return f"Content Uploaded"
        else:
            return render_template("igReuploader.html")

def showCurrentTime():
    print(f"Time: {datetime.now().strftime('%m')}-{datetime.now().strftime('%d')}-{datetime.now().strftime('%Y')} | {datetime.now().strftime('%H:%M:%S')}")

# reupload scheduler script
def feedStory():
    if feedStoryList:
        url = feedStoryList.pop(0)
        showCurrentTime()
        print("For Account: ", userName, "Feed Story, uploading: ", url) #print this to record last uplaoded
        reupload.reupload_function(cl, userName, url, "b")
        print(url, "Uploaded!")
    else:
        print("~~~All FeedStory have been uploaded. Stopping FeedStory scheduler.~~~")
        try:
            schedulerFeedStory.shutdown()
        except Exception:
            print ("Shutdown FeedStory Scheduler")
            pass
            
def story():
    for i in range(5):
        if feedStoryList:
            url = feedStoryList.pop(0)
            showCurrentTime()
            print(i+1, "For Account: ", userName, "Story, uploading: ", url) #print this to record last uplaoded
            reupload.reupload_function(cl, userName, url, "y")
            print(url, "Uploaded!")
        else:
            print("~~~All STORIES have been uploaded. Stopping Story scheduler.~~~")
            try:
                schedulerStory.shutdown()
            except Exception:
                print ("Shutdown Story Scheduler")
                pass
# reupload scheduler script 2
def feedStory2():
    if feedStoryList2:
        url = feedStoryList2.pop(0)
        showCurrentTime()
        print("For Account: ", userName2, "Feed Story, uploading: ", url) #print this to record last uplaoded
        reupload.reupload_function(cl2, userName2, url, "b")
        print(url, "Uploaded!")
    else:
        print("~~~All FeedStory have been uploaded. Stopping FeedStory scheduler.~~~")
        try:
            schedulerFeedStory.shutdown()
        except Exception:
            print ("Shutdown FeedStory Scheduler")
            pass

def story2():
    for i in range(6):
        if feedStoryList2:
            url = feedStoryList2.pop(0)
            showCurrentTime()
            print(i+1, "For Account: ", userName2, "Story, uploading: ", url) #print this to record last uplaoded
            reupload.reupload_function(cl2, userName2, url, "y")
            print(url, "Uploaded!")
        else:
            print("~~~All STORIES have been uploaded. Stopping Story scheduler.~~~")
            try:
                schedulerStory.shutdown()
            except Exception:
                print ("Shutdown Story Scheduler")
                pass


# Schedule the task to run every 10 seconds
schedulerFeedStory.add_job(feedStory, 'interval', hours=3) #upload to feed and story
schedulerFeedStory.start()
schedulerStory.add_job(story, 'interval', hours=24) #upload to story
schedulerStory.start()
schedulerFeedStory2.add_job(feedStory2, 'interval', hours=6) #upload to feed and story
schedulerFeedStory2.start()
schedulerStory2.add_job(story2, 'interval', hours=24) #upload to story
schedulerStory2.start()

# Register a function to shut down the scheduler when the Flask app exits
atexit.register(lambda: schedulerFeedStory.shutdown())
atexit.register(lambda: schedulerStory.shutdown())
atexit.register(lambda: schedulerFeedStory2.shutdown())
atexit.register(lambda: schedulerStory2.shutdown())

if __name__ == "__main__":
    cl, userName=igLogin.login_function()
    cl2, userName2=igLogin.login_function2()
    app.run(debug=False)

application = app