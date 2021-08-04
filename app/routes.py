from flask import render_template, request, redirect, url_for
import requests
from app import app
from .forms import LoginForm, RegisterForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                'first_name' : form.first_name.data.title(),
                'last_name' : form.last_name.data.title(),
                'email' : form.email.data.lower(),
                'password' : form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
        except:
            error_string = "There was a problem creating your account, please try again"
            return render_template('register.html.j2', form=form, error = error_string)
        return redirect(url_for('login'))
    return render_template('register.html.j2', form=form)


# used to display the login page - all the routes below
@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        print('Here')
        print(password)
        user_account = User.query.filter_by(email=email).first()
        print(user_account)
        if user_account is not None and user_account.check_hashed_password(password):
            login_user(user_account)
            return redirect(url_for('pokemon'))
        else:
            return redirect(url_for('login'))

        # if email in app.config.get('REGISTERED_USERS', {}).keys() and\
        #      password == app.config.get('REGISTERED_USERS', {}).get(email).get('password'):
        #      return f"Login was successful, Welcome {app.config.get('REGISTERED_USERS', {}).get(email).get('name')}"
        # error_string = "Incorrect Email/Password"
        return render_template("index.html.j2", form=form, error=error_string)
    return render_template("index.html.j2", form=form)
        


@app.route('/logout', methods=['GET', 'POST'])
@login_required        
def logout():
    if current_user:
        logout_user()
        return redirect(url_for('login'))



# used to display pokemon data
@app.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    if request.method == 'POST':
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        if not response.ok:
            # return -1
            error_string="Uh oh! Something went wrong"
            render_template("pokemon.html.j2", error=error_string)
        else:
            data = response.json()
            if not data:
                error_string=f"There is no Pokemon info for {name}, check the spelling"
                return render_template("pokemon.html.j2", error=error_string)
                # name, atleast one ability's name, base_experience, and 
                # the URL for its sprite
            complete_pokemon = []
            char_dict = {
                    "Name":data['forms'][0]['name'],
                    "Ability":data['abilities'][0]['ability']['name'],
                    "Base Experience":data['base_experience'], 
                    "Sprite URL":data['sprites']['front_shiny']
                    }
            complete_pokemon.append(char_dict)
            return render_template('pokemon.html.j2', pokemon=complete_pokemon)    
    return render_template("pokemon.html.j2")