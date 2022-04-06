from webtool import create_app
from flask import request
#import apportionment

app = create_app()

# WIP
@app.route('/apportionment')
def apportionment():
    print("here 1")
    return (request.form['id'])

# WIP 
@app.route('/allocation')
def allocation():
    print("here 2")
    return (request.form['id'])

# only if we run main.py, will we execute app.run()
if __name__ == '__main__':
    # run flask app on webserver, automatically rerun when we make changes
    app.run(debug=True)