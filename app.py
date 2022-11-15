from flask import Flask, redirect, render_template, request
from textfunctions import get_sentences

# Initialize flask 
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Stop browser from caching responses
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not (url):
            return redirect("/")
        
        # Get and display summary of Wiki page
        title, result = get_sentences(url)
        return render_template("result.html", result=result, title=title)
    else:
        return render_template("index.html")
        