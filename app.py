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
scheduler = BackgroundScheduler()
# schedulerFeedStory = BackgroundScheduler()
# schedulerStory = BackgroundScheduler()
# schedulerFeedStory2 = BackgroundScheduler()
# schedulerStory2 = BackgroundScheduler()
feedStoryList = URLS
feedStoryList2 = URLS2
cl= None
cl2= None
userName="DEFAULT1"
userName2="DEFAULT2"
job_schedule = {}

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
            print("Uploade Manualy Started, url:", url)
            if acc == "1":
                print("uploading for motiv...")
                reupload.reupload_function(cl, userName, url, story)
            elif acc == "2":
                print("uploading for car...")
                reupload.reupload_function(cl2, userName2, url, story)
            else:
                print ("acc query string not available or not valid, upload using default acc.")
                acc=1
                reupload.reupload_function(cl, userName, url, story)
            print("Application Stop Succesfuly.")
            return render_template("igReuploader.html", jobs=job_schedule, manual=acc)
        else:
            return render_template("igReuploader.html", jobs=job_schedule, manual=False)

def showCurrentTime():
    print(f"Time: {datetime.now().strftime('%m')}-{datetime.now().strftime('%d')}-{datetime.now().strftime('%Y')} | {datetime.now().strftime('%H:%M:%S')}")

def print_next_run_time(job_id):
    job = scheduler.get_job(job_id)
    if job:
        next_run = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
        job_schedule[job_id] = next_run
        # print(f"Next run of {job_id} is scheduled at {next_run}")
        print(job_schedule)

# reupload scheduler script
def feedStory():
    print("Run every 3h")
    if feedStoryList:
        url = feedStoryList.pop(0)
        showCurrentTime()
        print("For Account: ", userName, "Feed Story, uploading:", url) #print this to record last uplaoded
        reupload.reupload_function(cl, userName, url, "b")
        print(url, "Uploaded!")
        print_next_run_time("feedStory")
    else:
        print("~~~All FeedStory have been uploaded. Stopping FeedStory scheduler.~~~")
        # try:
        #     schedulerFeedStory.shutdown()
        # except Exception:
        #     print ("Shutdown FeedStory Scheduler")
        #     pass
            
def story():
    print("Run every 24h")
    for i in range(5):
        if feedStoryList:
            url = feedStoryList.pop(0)
            showCurrentTime()
            print(i+1, "For Account: ", userName, "Story, uploading:", url) #print this to record last uplaoded
            reupload.reupload_function(cl, userName, url, "y")
            print(url, "Uploaded!")
        else:
            print("~~~All STORIES have been uploaded. Stopping Story scheduler.~~~")
            # try:
            #     schedulerStory.shutdown()
            # except Exception:
            #     print ("Shutdown Story Scheduler")
            #     pass
    print_next_run_time("story")
# reupload scheduler script 2
def feedStory2():
    print("Run every 5H")
    if feedStoryList2:
        url = feedStoryList2.pop(0)
        showCurrentTime()
        print("For Account: ", userName2, "Feed Story, uploading:", url) #print this to record last uplaoded
        reupload.reupload_function(cl2, userName2, url, "b")
        print(url, "Uploaded!")
        print_next_run_time("feedStory2")
    else:
        print("~~~All FeedStory have been uploaded. Stopping FeedStory scheduler.~~~")
        # try:
        #     schedulerFeedStory2.shutdown()
        # except Exception:
        #     print ("Shutdown FeedStory Scheduler")
        #     pass

def story2():
    print("Run every 24h")
    for i in range(5):
        if feedStoryList2:
            url = feedStoryList2.pop(0)
            showCurrentTime()
            print(i+1, "For Account: ", userName2, "Story, uploading:", url) #print this to record last uplaoded
            reupload.reupload_function(cl2, userName2, url, "y")
            print(url, "Uploaded!")
        else:
            print("~~~All STORIES have been uploaded. Stopping Story scheduler.~~~")
            # try:
            #     schedulerStory2.shutdown()
            # except Exception:
            #     print ("Shutdown Story Scheduler")
            #     pass
    print_next_run_time("story2")


scheduler.add_job(feedStory, 'interval', hours=3, id='feedStory')
scheduler.add_job(story, 'interval', hours=24, id='story')
scheduler.add_job(feedStory2, 'interval', hours=5, id='feedStory2')
scheduler.add_job(story2, 'interval', hours=23, id='story2')
scheduler.start()

# Register a function to shut down the scheduler when the Flask app exits
# atexit.register(lambda: schedulerFeedStory.shutdown())
# atexit.register(lambda: schedulerStory.shutdown())
# atexit.register(lambda: schedulerFeedStory2.shutdown())
# atexit.register(lambda: schedulerStory2.shutdown())
atexit.register(lambda: scheduler.shutdown())

for job in scheduler.get_jobs():
    next_run = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
    job_schedule[job.id] = next_run
    print(f"Job {job.id} scheduled to run at {next_run}")
print(job_schedule)

if __name__ == "__main__":
    print("Start login")
    # userName = "user1"
    # userName2 = "user2"
    cl, userName=igLogin.login_function()
    cl2, userName2=igLogin.login_function2()

    app.run(debug=False)

application = app