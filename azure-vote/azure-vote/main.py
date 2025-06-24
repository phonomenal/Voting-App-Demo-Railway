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

# Storage configuration - Redis or in-memory fallback
redis_url = os.environ.get('REDIS_URL')
redis_server = os.environ.get('REDIS', os.environ.get('REDIS_HOST'))
redis_port = int(os.environ.get('REDIS_PORT', '6379'))
redis_password = os.environ.get('REDIS_PWD', os.environ.get('REDIS_PASSWORD', None))

# In-memory storage fallback
vote_storage = {}

# Redis Connection with fallback
use_redis = False
r = None

if redis_url or redis_server:
    try:
        if redis_url:
            # Use Redis URL if provided (Upstash, Heroku style)
            r = redis.from_url(redis_url, decode_responses=True)
        elif redis_server:
            if redis_password:
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
        use_redis = True
        print("✅ Connected to Redis")
    except (redis.ConnectionError, Exception) as e:
        print(f"⚠️  Redis connection failed: {e}")
        print("📝 Falling back to in-memory storage")
        use_redis = False
else:
    print("📝 No Redis configured, using in-memory storage")

# Storage helper functions
def get_vote_count(key):
    if use_redis:
        return r.get(key) or '0'
    else:
        return str(vote_storage.get(key, 0))

def set_vote_count(key, value):
    if use_redis:
        r.set(key, value)
    else:
        vote_storage[key] = int(value)

def increment_vote(key):
    if use_redis:
        r.incr(key, 1)
    else:
        vote_storage[key] = vote_storage.get(key, 0) + 1

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Initialize vote counts
if not get_vote_count(button1) or get_vote_count(button1) == '0':
    set_vote_count(button1, 0)
if not get_vote_count(button2) or get_vote_count(button2) == '0':
    set_vote_count(button2, 0)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        # Get current values
        vote1 = get_vote_count(button1)
        vote2 = get_vote_count(button2)
        # Return index with values
        return render_template(
            "index.html", value1=int(vote1),
            value2=int(vote2), button1=button1,
            button2=button2, title=title)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            # Empty table and return results
            set_vote_count(button1, 0)
            set_vote_count(button2, 0)
            vote1 = get_vote_count(button1)
            vote2 = get_vote_count(button2)
            return render_template(
                "index.html", value1=int(vote1), value2=int(vote2),
                button1=button1, button2=button2, title=title)
        else:

            # Insert vote result into storage
            vote = request.form['vote']
            increment_vote(vote)
            # Get current values
            vote1 = get_vote_count(button1)
            vote2 = get_vote_count(button2)
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
