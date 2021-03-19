from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/disciplines')
def disciplines():
    return render_template('disciplines.html')

@app.route('/time_schedule')
def time_schedule():
    return render_template('time_schedule.html')

@app.route('/image_gallery')
def image_gallery():
    return render_template('image_gallery.html')

@app.route('/news')
def news():
    return render_template('news.html')
