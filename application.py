# APPlICATION FILE FOR 3155 PROJECT

import os  # os is used to get environment variables IP & PORT

import bcrypt
from flask import Flask, redirect, url_for  # Flask is the web app that we will customize
from flask import render_template
from flask import request
from database import db
from models import User as User
from models import Event as Event
from models import RSVP as RSVP
from models import Invite as Invite
from models import Rating as Rating
from models import Friend as Friend
from forms import RegisterForm
from forms import LoginForm
from flask import session


app = Flask(__name__)  # create an app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_project_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'

db.init_app(app) # initializes database


with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index')
def index():
    # to be implemented
    # check if a user is saved in session
    if session.get('user'):
        return render_template("index.html", user=session['user'])
    return render_template("index.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    # to be implemented
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.fName
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_events'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(request.form['email'], first_name, last_name, h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_events'))

    # something went wrong - display register view
    return render_template('register.html', form=form)

@app.route('/events')
def get_events():
    # check if a user is saved in session
    if session.get('user'):
        # retrieve events from database
        my_events = db.session.query(Event).filter_by(user_id=session['user_id']).order_by(Event.id).all()
        public_events = db.session.query(Event).filter_by(public=True).order_by(Event.id).all()

        my_invitations = db.session.query(Invite).filter_by(user_id=session['user_id'])
        invited_event_ids = []

        for invitation in my_invitations:
            invited_event_ids.append(invitation.event_id)

        invited_events = db.session.query(Event).filter(Event.id.in_(invited_event_ids))

        my_set = set(my_events)
        public_set = set(public_events)
        public_and_unique = list(public_set - my_set)

        return render_template('events.html', events=my_events, user=session['user'], public_events=public_and_unique,
                               invited_events=invited_events)
    else:
        return redirect(url_for('login'))

@app.route('/events/<event_id>')
def get_event(event_id):
    # check if a user is saved in session
    if session.get('user'):
        # retrieve event from database
        my_event = db.session.query(Event).filter_by(id=event_id).one()
        my_rsvps = db.session.query(RSVP).filter_by(event_id=event_id)
        my_ratings = db.session.query(Rating).filter_by(event_id=event_id)

        # create a comment form object

        return render_template('event.html', event=my_event, rsvps=my_rsvps, ratings=my_ratings, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    # check if a user is saved in session
    if session.get('user'):
        # check method used for request
        if request.method == 'POST':
            # get title data
            event_name = request.form['event_name']
            # get note data
            event_details = request.form['event_details']
            # get event start date
            start_date = request.form['start_date']
            #get event end date
            end_date = request.form['end_date']

            #public_str = request.form['public']
            #public = (public_str == 'Y')
            public = False
            if request.form.get('public'):
                public = True

            new_record = Event(session['user_id'], event_name, event_details.strip(), start_date, end_date, public)
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('get_events'))
        else:
            # GET request - show new note form
            return render_template('new.html', user=session['user'])
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/events/edit/<event_id>', methods=['GET', 'POST'])
def update_event(event_id):
    # check if a user is saved in session
    if session.get('user'):
        # check method used for request
        if request.method == 'POST':
            # get title data
            event_name = request.form['event_name']
            # get event data
            event_details = request.form['event_details']
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            # checks updates to public / private
            #public_str = request.form['public']
            #public_str = public_str.strip()
            #public = (public_str == 'Y')
            public = False
            if request.form.get('public') is not None:
                public = True

            #get event
            event = db.session.query(Event).filter_by(id=event_id).one()


            # update note data
            # also removes leading whitespace from form input
            event.event_name = event_name.strip()
            event.event_details = event_details.strip()
            event.start_date = start_date.strip()
            event.end_date = end_date.strip()
            event.public = public

            # update event in DB
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('get_events'))
        else:
            # GET request - show new event form to edit event

            # retrieve event from database
            my_event = db.session.query(Event).filter_by(id=event_id).one()

            return render_template('new.html', event=my_event, user=session['user'])
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/events/delete/<event_id>', methods=['POST'])
def delete_event(event_id):
    # check if a user is saved in session
    if session.get('user'):
        # retrieve event from database
        my_event = db.session.query(Event).filter_by(id=event_id).one()

        db.session.delete(my_event)
        db.session.commit()

        return redirect(url_for('get_events'))
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/unfinished')
def not_done_yet():
    return render_template('not_done_yet.html')

@app.route('/share/<event_id>', methods=['POST', 'GET'])
def share(event_id):

    # check if a user is saved in session
    if session.get('user'):

        if request.method == 'POST':

            user_email = request.form['email']

            user = db.session.query(User).filter_by(email=user_email).first()
            user_id = user.id

            invitation = Invite(user_email, user_id, event_id)

            # add new email object to database
            db.session.add(invitation)
            db.session.commit()

            return redirect(url_for('get_events', user=session['user']))
        else:
            return render_template('share.html', event_id=event_id, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/rsvp/<event_id>', methods=['GET', 'POST'])
def rsvp(event_id):


    # check if user is signed in
    if session.get('user'):

        # checks if form response is of type POST
        if request.method == 'POST':


            user_id=session['user_id']

            # get date RSVPed
            from datetime import datetime
            rsvp_date = datetime.now()

            # get response to if the user is attending
            status_str = request.form['status'].strip()
            status = (status_str == 'Y')


            # create RSVP object with given data
            rsvp_user=db.session.query(User).filter_by(id=session['user_id']).one()
            user_name = rsvp_user.fName + " " + rsvp_user.lName

            rsvp = RSVP(user_id, user_name, event_id, rsvp_date, status)


            # add new RSVP object to database
            db.session.add(rsvp)
            db.session.commit()

            # redirects back to events page ((may implement a success page))
            return redirect(url_for('get_events'))
        else:

            # if user has already RSVPed, redirects to edit rsvp
            if db.session.query(RSVP).filter_by(event_id= event_id, user_id=session['user_id']).count() != 0:
                return redirect(url_for('edit_rsvp', event_id=event_id))

            my_event = db.session.query(Event).filter_by(id=event_id).one()

            # redirects user to blank form if method type is GET
            return render_template('rsvp.html', event=my_event, user=session['user'])
    else:
        # user is not signed in, redirect to sign in

        return redirect(url_for('login'))

@app.route('/edit_rsvp/<event_id>', methods=['GET', 'POST'])
def edit_rsvp(event_id):
    # check if user is signed in
    if session.get('user'):

        # checks if form response is of type POST
        if request.method == 'POST':

            # get response to if the user is attending
            status_str = request.form['status'].strip()
            status = (status_str == "Y")

            # gets existing RSVP with event id and user id
            rsvp = db.session.query(RSVP).filter_by(event_id= event_id, user_id=session['user_id']).one()

            # updates existing RSVP with new user data
            rsvp.status = status

            # commit change to db
            db.session.add(rsvp)
            db.session.commit()

            # redirects back to events page
            return redirect(url_for('get_events'))
        else:
            # gets event and corresponding RSVP
            my_rsvp = db.session.query(RSVP).filter_by(event_id=event_id, user_id=session['user_id'])
            my_event = db.session.query(Event).filter_by(id=event_id).one()

            # redirects user to blank form if method type is GET, passes RSVP with user id and event id
            return render_template('rsvp.html', event=my_event, user=session['user'], rsvp=my_rsvp)
    else:
        # user is not signed in, redirect to sign in

        return redirect(url_for('login'))


@app.route('/rate/<event_id>', methods=['GET', 'POST'])
def rate(event_id):

    # check if user is signed in
    if session.get('user'):

        # checks if form response is of type POST
        if request.method == 'POST':
            user_id=session['user_id']


            # get response to user rating
            rating_no = request.form['rating']

            # create RSVP object with given data
            rsvp_user=db.session.query(User).filter_by(id=session['user_id']).one()
            user_name = rsvp_user.fName + " " + rsvp_user.lName

            rating = Rating(user_name, user_id, event_id, rating_no)


            # add new Rating object to database
            db.session.add(rating)
            db.session.commit()

            # redirects back to events page ((may implement a success page))
            return redirect(url_for('get_events'))
        else:
            my_event = db.session.query(Event).filter_by(id=event_id).one()

            # redirects user to blank form if method type is GET
            return render_template('rate.html', event=my_event, user=session['user'])
    else:
        # user is not signed in, redirect to sign in
        return redirect(url_for('login'))

@app.route('/friends/new', methods=['GET', 'POST'])
def add_friend():
    if session.get('user'):

        if request.method == 'POST':

            email = request.form["email"].strip()
            friend = db.session.query(User).filter_by(email=email).first()


            if friend is not None:

                user_id = session['user_id']

                new_friend = Friend(user_id, friend.id)

                db.session.add(new_friend)
                db.session.commit()

                return redirect(url_for('get_friends', user=session['user']))

            else:
                return redirect(url_for('get_friends', user=session['user']))


        else:
            return render_template('newfriend.html', user=session['user'])

    else:
        # user is not signed in, redirect to sign in
        return redirect(url_for('login'))

@app.route('/friends')
def get_friends():
    if session.get('user'):

        friends_of_user = db.session.query(Friend).filter_by(user_id=session['user_id']).all()

        friend_ids = []

        for friend in friends_of_user:
            friend_ids.append(friend.friend_id)

        friends_list = db.session.query(User).filter(User.id.in_(friend_ids))

        return render_template("friends.html", friends=friends_list, user=session['user'])

    else:
        # user is not signed in, redirect to sign in
        return redirect(url_for('login'))

@app.route('/friend/<friend_id>')
def show_friend(friend_id):
    # check if a user is saved in session
    if session.get('user'):
        # retrieve event from database

        friend_events = db.session.query(Event).filter_by(user_id=friend_id)
        friend = db.session.query(User).filter_by(id=friend_id).one()


        return render_template('friend.html', events=friend_events, user=session['user'], friend=friend)

    else:
        return redirect(url_for('login'))

@app.route('/search/<query>')
def search_result(query):
    # check if a user is saved in session
    if session.get('user'):
        # retrieve event from database

        search = "%{}%".format(query)

        search_result = db.session.query(Event).filter(Event.event_name.like(search))

        return render_template('searchresult.html', events=search_result, user=session['user'])

    else:
        return redirect(url_for('login'))

@app.route("/search", methods=['GET', 'POST'])
def search():
    # check if a user is saved in session
    if session.get('user'):
        # retrieve event from database
        if request.method == 'POST':
            query= request.form["searchBar"]
            return redirect(url_for("search_result", query=query))

        else:
            return render_template('search.html', user=session['user'])

    else:
        return redirect(url_for('login'))



app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
