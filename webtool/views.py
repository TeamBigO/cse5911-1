# store standard routes (where users can go) on our website
from flask import Blueprint, render_template, request, flash

views = Blueprint('views', __name__)

# define view for home page - runs whenever we go to / route
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # get all info from form
        id = request.form.get('id')
        likely_voters = request.form.get('LV')
        eligible_voters = request.form.get('EV')
        ballot_length = request.form.get('BL')

        if id.isdigit() and likely_voters.isdigit() and eligible_voters.isdigit() and ballot_length.isdigit():
            # add inputs to database??
            flash('Success!', category='success')
        else:
            # error with input - flash a message
            flash('Input values must be valid numbers.', category='error')
    return render_template("home.html")

@views.route('/tutorial')
def tutorial():
    return render_template("help.html")

@views.route('/about')
def about():
    return render_template("settings.html", settings="Testing", wait_time=10, boolean=True)