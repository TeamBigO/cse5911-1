# store standard routes (where users can go) on our website
from flask import Blueprint, render_template, request, flash

views = Blueprint('views', __name__)

# define view for home page - runs whenever we go to / route
@views.route('/', methods=['GET', 'POST'])
def home():
    #data = request.form  #immutable dict
    #print(data)

    if request.method == 'POST':
        # get all info from form
        id = request.form.get('id')
        likely_voters = request.form.get('LV')
        eligible_voters = request.form.get('EV')
        ballot_length = request.form.get('BL')

        # parse inputs from strings (which are columns pasted from Excel)
        id_list, lv_list, ev_list, bl_list = [s for s in id.split() if s.isdigit()], [s for s in likely_voters.split() if s.isdigit()], [s for s in eligible_voters.split() if s.isdigit()], [s for s in ballot_length.split() if s.isdigit()]

        print(id_list)
        print(lv_list)
        print(ev_list)
        print(bl_list)

        #if id.isdigit() and likely_voters.isdigit() and eligible_voters.isdigit() and ballot_length.isdigit():
        if len(id_list) == len(lv_list) == len(ev_list) == len(bl_list):
            # add inputs to database??
            flash('Success!', category='success')

            # input to apportionment + allocation => dict of dicts
            # WIP, this will likely go in apportionment + allocation instead
            input_data = dict()
            for (i, item) in enumerate(id_list):
                loc_dict = {'Likely or Exp. Voters': int(lv_list[i]), 'Eligible Voters': int(ev_list[i]), 'Ballot Length Measure': int(bl_list[i])}

                input_data[int(item)] = loc_dict
                #print(input_data)
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
