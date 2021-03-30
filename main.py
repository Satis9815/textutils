from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+mysqlconnector://root:@localhost/contacts"
app.config['SECRET_KEY'] = "saris"
db=SQLAlchemy(app)


class Details(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80) ,nullable=False)
    phone_num = db.Column(db.Integer, nullable=False)
    self_desc = db.Column(db.String(180),  nullable=False)
    description = db.Column(db.String(500),  nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/", methods=['GET','POST'])
def home():
    ftext=request.form.get('formtext')
    if(request.method=='POST'):
        frempunc=request.form.get('rempunc','off')
        fullupercase=request.form.get('uppercase','off')
        newLineRemover=request.form.get('newlineremover','off')
        fulllowercase=request.form.get('lowercase','off')
        extraSpaceRemover=request.form.get('extraspaceremover','off')
        charCounter=request.form.get('charcounter','off')

        if frempunc=="on":
            analyzed=""
            punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            for char in ftext:
                if char not in punctuations:
                    analyzed=analyzed+char
            params={'purpose':'Remove Punctuations','analyzed_text':analyzed}
            return render_template('analyzed.html',params=params)

        elif(fullupercase=="on"):
            analyzed=""
            for char in ftext:
                analyzed=analyzed+char.upper()
            params={'purpose':'Change to Uppercase','analyzed_text':analyzed}
            return render_template('analyzed.html',params=params)

        elif(fullupercase=="on"):
            analyzed=""
            for char in ftext:
                analyzed=analyzed+char.upper()
            params={'purpose':'Change to Uppercase','analyzed_text':analyzed}
            return render_template('analyzed.html',params=params)


        elif(newLineRemover=="on"):
            analyzed=""
            for char in ftext:
                if char !="\n" and char !="\r":
                    analyzed = analyzed+char
            params={'purpose':'Remove the new line','analyzed_text':analyzed}
            return render_template('analyzed.html',params=params)


        elif(fulllowercase=="on"):
            analyzed=""
            for char in ftext:
                analyzed=analyzed+char.lower()
            params={'purpose':'Change to lowercase','analyzed_text':analyzed}
            return render_template('analyzed.html',params=params)


        elif(extraSpaceRemover=="on"):
            analyzed=""
            for index,char in enumerate(ftext):
                if not(ftext[index]==" " and ftext[index+1]==" "):
                    analyzed=analyzed+char
            params={'purpose':'Remove extra space','analyzed_text':analyzed}
            return render_template('analyzed.html',params=params)


        elif(charCounter=="on"):
            analyzed=len(ftext)
            params={'purpose':'Total number of charater ','analyzed_text':analyzed}
            return render_template('analyzed.html',params=params)
        else:
            return render_template("error.html")
    return render_template('index.html')
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        femail=request.form.get('email')
        fphone=request.form.get('phone')
        fsefldesc=request.form.get('selfdesc')
        fdescription=request.form.get('description')
        details=Details(email=femail,phone_num=fphone,self_desc=fsefldesc,description=fdescription,date=datetime.now())
        db.session.add(details)
        db.session.commit()
    return render_template("contact.html")
app.run(debug=True)