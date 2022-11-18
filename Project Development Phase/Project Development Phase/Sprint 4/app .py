from flask import Flask, request, render_template, redirect, url_for
from cloudant.client import Cloudant


#from detect import my_database
client = Cloudant.iam('6c89a0da-d603-41e5-a40b-6af61327e9af-bluemix', 'CiLg1OOKnQVKb0S7KJT-rdxsDAvGezjZw1tOjV2tXuFX', connect =True)

my_database = client.create_database('my_database')
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/home.html')
def home():
    return render_template("home.html")


@app.route('/signup')
def register():
    return render_template('signup.html')


@app.route('/after_signup', methods=['post'])
def after_reg():
    x = [x for x in request.form.values()]
    print(x)
    data = {
        '_id': x[1],
        'name': x[0],
        'psw': x[2],

    }
    print(data)
    query = {'_id': {'$eq': data['_id']}}

    docs = my_database.get_query_result(query)
    print(docs)

    print(len(docs.all()))

    if len(docs.all()) == 0:
        url = my_database.create_document(data)
        # response = requests.get(url)
        return render_template('index.html', pred="Registration Successful, please login using your details")
    else:
        return render_template('index.html', pred="You are already a member, please login using your details")


@app.route('/signin')
def login():
    return render_template('signin.htmL')


@app.route('/after_signin', methods=['POST'])
def after_login():
    user = request.form['_id']
    passe = request.form['psw']
    print(user, passe)

    query = {'_id': {'$eq': user}}
    docs = my_database.get_query_result(query)
    print(docs)

    print(len(docs.all()))

    if len(docs.all()) == 0:
        return render_template('signin.html', pred="The username is not found.")
    else:
        if user == docs[0][0]['_id'] and passe == docs[0][0]['psw']:
            return render_template('index.html')
        else:
            print('Invalid User')

@app.route('/about1')
def about1():
    return render_template('about1.html')

@app.route('/job-detail')
def jobdetail():
    return render_template('job-detail.htmL')

@app.route('/about')
def about():
    return render_template('about.htmL')

@app.route('/category')
def category():
    return render_template('category.htmL')

@app.route('/contact')
def contact():
    return render_template('contact.htmL')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')


@app.route('/job-list')
def joblist():
    return render_template('job-list.html')






if __name__== "__main__":
    app.run(debug=True)