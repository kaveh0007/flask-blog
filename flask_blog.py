from flask import Flask, render_template
from forms import RegistrationForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cbd535a731c27deae6fc9e9c2fbb12225cb321c530fddcf272c6a606b24dca58'

Posts = [
    {
        'author': 'Kaveh',
        'title': 'Blog Post 1',
        'date_posted': 'October 24, 2025',
        'content': 'Hello this is my first blog post'
    },

    {
        'author': 'John Doe',
        'title' : 'Blog Post 1',
        'date_posted' : 'October 24, 2025',
        'content' : 'Hello now the AWS server in east US just went down'
    }
]

@app.route('/')
def home():
    return render_template('home.html', posts=Posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/health')
def health_check():
    return 'The backend is running'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form, title='Sign Up')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')