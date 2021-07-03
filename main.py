from flask import Flask, render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
import json, datetime

with open('config.json', 'r') as c:
    para= json.load(c)["params"]


app= Flask(__name__)
app.secret_key= 'super-secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = para['local_url']
db= SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    mes = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(80),  nullable=True)
    date= db.Column(db.String(20),  nullable=False)



class Post(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user = db.Column(db.String(80), nullable=False)
    tagline = db.Column(db.String(80), nullable=False)
    slung = db.Column(db.String(120), nullable=True)
    content = db.Column(db.String(120), nullable=False)
    date= db.Column(db.String(20),  nullable=False)
    img_file= db.Column(db.String(20),  nullable=True)


@app.route('/')
def home ():
    k=len(Post.query.filter_by().all())
    posts= Post.query.filter_by().all()[k-para['no_of_post']:k]
    return render_template('index.html', para=para, posts=posts)

@app.route('/about')

def about ():
    
 

    return render_template('about.html', para=para)

@app.route('/contacts', methods=['GET', 'POST'])


def contact ():
    if(request.method=='POST' ):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        mes= request.form.get('message')
        entry= Contact(name= name, phone= phone,mes= mes,email= email)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html',para=para)

@app.route('/post/<string:post_slung>', methods=['GET'])
def post_route (post_slung):
    post1= Post.query.filter_by(slung=post_slung).first()

    return render_template('post.html', para=para,post1= post1)
# @app.route('/post')
# def post():
#   return render_template('post.html',post1=post1)
@app.route('/olderpost')
def homey ():
    k=len(Post.query.filter_by().all())
    k= k-para['no_of_post']
    # k=len(Post.query.filter_by().all())-para['no_of_post']
    posts= Post.query.filter_by().all()[k-para['no_of_post']:k]
    return render_template('index.html', para=para, posts=posts)

@app.route('/login')
def log():
    return render_template("login.html")

@app.route('/auth', methods=['POST'])
def auth():
    posts= Post.query.all()
    if('user' in session and session['user'] == para["user_name"]):
        return render_template("dashboard.html", para=para, posts=posts)
    if(request.method == 'POST'):
        name= request.form.get('uname')
        passs= request.form.get('psw')
        if(name == para["user_name"] and passs == para["password"]):
            session['user']= name
            return render_template("dashboard.html", para=para, posts=posts)
        else:
            # print('enter correct credentials')
            return render_template('error.html')

@app.route('/edit/<string:sno>', methods= ['GET','POST'])

def edit1(sno):
    posts=Post.query.filter_by(sno=sno).first()
    if('user' in session and session['user'] == para["user_name"]):
        if(request.method== 'POST'):
            title1= request.form.get('title')
            tagline= request.form.get('tagline')
            content= request.form.get('content')
            user= request.form.get('user')
            if(sno=='0'):
                date= datetime.datetime.now()
                posts= Post(title=title1, tagline= tagline,content= content, user= user, date= date)
                db.session.add(posts)
                db.session.commit()
            else:
                posts.title= title1
                posts.tagline= tagline
                posts.content= content
                posts.user= user
                db.session.commit()
        return render_template("edit.html", posts=posts, para= para,sno=sno)

@app.route('/delete/<string:sno>', methods= ['GET','POST'])

def deleting(sno):
    if('user' in session and session['user'] == para["user_name"]):
        posts= Post.query.all()
        l= Post.query.filter_by(sno=sno).first()
        db.session.delete(l)
        db.session.commit()
   

        return redirect("/auth")

@app.route('/logout')

def logout():
    session.pop('user',None)
    return redirect('/login')











if(__name__=="__main__"):
    app.run(debug= True)
