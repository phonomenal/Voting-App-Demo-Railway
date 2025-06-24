from flask import Flask, request, render_template
import os
# import random
import redis
import socket
# import sys

app = Flask(__name__)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

if ("VOTE1VALUE" in os.environ and os.environ['VOTE1VALUE']):
    button1 = os.environ['VOTE1VALUE']
else:
    button1 = app.config['VOTE1VALUE']

if ("VOTE2VALUE" in os.environ and os.environ['VOTE2VALUE']):
    button2 = os.environ['VOTE2VALUE']
else:
    button2 = app.config['VOTE2VALUE']

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

# Redis configurations
# Support multiple Redis connection formats for different cloud providers
redis_server = os.environ.get('REDIS', os.environ.get('REDIS_HOST', 'localhost'))
redis_port = int(os.environ.get('REDIS_PORT', '6379'))
redis_password = os.environ.get('REDIS_PWD', os.environ.get('REDIS_PASSWORD', None))

# Handle Redis URL format (common in cloud services)
redis_url = os.environ.get('REDIS_URL')

# Redis Connection
try:
    if redis_url:
        # Use Redis URL if provided (Railway, Heroku style)
        r = redis.from_url(redis_url)
    elif redis_password:
        # Use password authentication
        r = redis.StrictRedis(
                    host=redis_server,
                    port=redis_port,
                    password=redis_password,
                    decode_responses=True)
    else:
        # Local development or no auth
        r = redis.Redis(host=redis_server, port=redis_port, decode_responses=True)
    r.ping()
except redis.ConnectionError:
    print(f'Failed to connect to Redis at {redis_server}:{redis_port}')
    exit('Failed to connect to Redis, terminating.')

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Init Redis
if not r.get(button1):
    r.set(button1, 0)
if not r.get(button2):
    r.set(button2, 0)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        # Get current values
        vote1 = r.get(button1) or '0'
        vote2 = r.get(button2) or '0'
        # Return index with values
        return render_template(
            "index.html", value1=int(vote1),
            value2=int(vote2), button1=button1,
            button2=button2, title=title)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            # Empty table and return results
            r.set(button1, 0)
            r.set(button2, 0)
            vote1 = r.get(button1) or '0'
            vote2 = r.get(button2) or '0'
            return render_template(
                "index.html", value1=int(vote1), value2=int(vote2),
                button1=button1, button2=button2, title=title)
        else:

            # Insert vote result into DB
            vote = request.form['vote']
            r.incr(vote, 1)
            # Get current values
            vote1 = r.get(button1) or '0'
            vote2 = r.get(button2) or '0'
            # Return results
            return render_template(
                "index.html", value1=int(vote1), value2=int(vote2),
                button1=button1, button2=button2, title=title)


if __name__ == "__main__":
    # Get port from environment variable for cloud deployment
    port = int(os.environ.get('PORT', 5000))
    # Enable debug mode only in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
