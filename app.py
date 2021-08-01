from flask import Flask, render_template, request
import requests

app = Flask(__name__)

app.config.update(
    REGISTERED_USERS = {
        'kevinb@codingtemple.com':{"name":"Kevin","password":"abc123"},
        'johnl@codingtemple.com':{"name":"John", "password":"Colt45"},
        'joelc@codingtemple.com':{"name":"Joel","password":"MorphinTime"}
    }
)

# used to display the login page
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
        if email in app.config.get('REGISTERED_USERS', {}).keys() and\
             password == app.config.get('REGISTERED_USERS', {}).get(email).get('password'):
             return f"Login was successful, Welcome {app.config.get('REGISTERED_USERS', {}).get(email).get('name')}"
        error_string = "Incorrect Email/Password"
        return render_template("index.html.j2", error=error_string)
    return render_template("index.html.j2")
        


# used to display pokemon data
@app.route('/pokemon', methods=['GET', 'POST'])
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