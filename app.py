
import mysql.connector as m
from flask import Flask,render_template,session,request,redirect

db=m.connect(
    host='localhost',
    user='root',
    password='root',
    database='gopi'
)
cur=db.cursor()

app=Flask(__name__)
app.secret_key='gopi'

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/register')
def registerpage():
    return render_template('register.html')

@app.route('/SignUp',methods=['POST'])
def SignUp():
    email=request.form['email']
    uid=request.form['uid']
    uname=request.form['uname']
    psw=request.form['psw']
    
    sql="insert into notelyuser values(%s,%s,%s,%s)"
    val=(email,uid,uname,psw)
    try:
        cur.execute(sql,val)
    except:
        return render_template('register.html',res='sorry unable to create a account')
    db.commit()
    return redirect('/login')
    return render_template("register.html",res="account created successfully")
    

@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/validatelogin',methods=['POST'])
def validatelogin():
    uid=request.form['uid']
    upass=request.form['psw']
    sql="select upass from notelyuser where uid=%s"
    val=(uid,)
    cur.execute(sql,val)
    result=cur.fetchall()
    if len(result)!=0:
        if result[0][0]==upass:
            session['uid']=uid
            return render_template('loginaccount.html',res=uid)
        else:
            return render_template('login.html',res="please provide correct password")
    else:
        return render_template('login.html',res="please provide valid details for login to your account")

@app.route('/loginaccount')
def loginaccount():
    return render_template('loginaccount.html')

@app.route('/createnote')
def createnote():
    return render_template('createnote.html')

@app.route('/submitcreatenote',methods=['POST'])
def submitcreatenote():
    sub1=request.form['sub']
    if sub1=="yes":
        uid=session['uid']
        usubject=request.form['subject']
        unotes=request.form['notes']
        sql="insert into note values(%s,%s,%s)"
        val=(uid,usubject,unotes)
        try:
            cur.execute(sql,val)
        except:
            return render_template('createnote.html',res='notes not created')
        db.commit()
        return redirect('/MyNotes')
    else:
        return redirect('/createnote')

@app.route('/MyNotes')
def MyNotes():
    uid=session['uid']
    sql='select sub,notes from note where uid=%s'
    val=(uid,)
    cur.execute(sql,val)
    result=cur.fetchall()
    if len(result)!=0:
        return render_template('mynotes.html',res=result)
    else:
        return render_template('create.html',res="You don't have any notes..Please create a notes")
   
@app.route('/mynotes')
def mynotes():
    return render_template('mynotes.html')

@app.route('/mysub',methods=['POST'])
def mysub():
    mysub1=request.form['sub']
    uid1=session['uid']
    sql='select sub,notes from note where uid=%s and sub=%s'
    val=(uid1,mysub1)
    cur.execute(sql,val)
    res1=cur.fetchall()
    return render_template('mysubnotes.html',res=res1)

@app.route('/mysubnotes')
def mysubnotes():
    return render_template('mysubnotes.html')

@app.route('/modifynotes',methods=['POST'])
def modifynotes():
    mysub1=request.form['sub']
    notes=request.form['note']
    uid1=session['uid']
    u=request.form['but']
    if u=='NO':
        return redirect('/MyNotes')
    elif u=='delete':
        sql='delete from note where uid=%s and sub=%s'
        val=(uid1,mysub1)
        try:
            cur.execute(sql,val)
            db.commit()
            return redirect('/MyNotes')
        except:
            return render_template('mysubnotes.html',res='unable to delete')
    elif u=='UAS':
        sql='update note set notes=%s where sub=%s and uid=%s'
        val=(notes,mysub1,uid1)
        try:
            cur.execute(sql,val)
            db.commit()
            return redirect('/MyNotes')
        except:
             return render_template('mysubnotes.html',res='unable to update')
