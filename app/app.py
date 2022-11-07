from flask import Flask
import os
import socket
import time
import datetime

from sqlalchemy import create_engine

db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'

# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

def add_new_row(n):
    # Insert a new number into the 'numbers' table.
    db.execute("INSERT INTO numbers (number,timestamp) "+\
        "VALUES ("+\
        str(n) + "," + \
        str(int(round(time.time() * 1000))) + ");")

def get_last_row():
    # Retrieve the last number inserted inside the 'numbers'
    query = "" + \
            "SELECT *" + \
            "FROM numbers " + \
            "WHERE timestamp >= (SELECT max(timestamp) FROM numbers)" +\
            "LIMIT 1"
    result_set = db.execute(query)  
    for (r) in result_set:  
        return str(r[0])+' - '+str(datetime.datetime.fromtimestamp(round(r[1]/1000)))+' (UTC)'

app = Flask(__name__)

@app.route("/about")
def about(): 
    html = "<h3>Hello!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())
    
count = 0
add_new_row(count)
    
@app.route('/', methods=['GET'])
def home():
    add_new_row(count)
    return str(count)
    
@app.route('/stat', methods=['GET'])
def stat():
    global count
    count+=1
    add_new_row(count)
    return str(count)
    
@app.route('/last', methods=['GET'])
def last():
    return str('The last count is: {}'.format(get_last_row()))

if __name__ == "__main__":
    app.run(host='0.0.0.0')