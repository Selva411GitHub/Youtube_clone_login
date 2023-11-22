from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3 as sql

app=Flask(__name__)

app.secret_key = "selva411"


@app.route('/')
def youtubehome():
    conn=sql.connect('videos.db')
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("Select * from videos_table")
    data=cur.fetchall()
    return render_template('youtubu.html',data=data)


@app.route('/play')
def youtubeplayed():
    return render_template('videoplayer.html')

@app.route('/add',methods=['POST','GET'])
def youtubeadd():
    if request.method =='POST':
        name = request.form['name']
        thumbnaildp = request.form['thumbnaildp']
        thumbnail = request.form['thumbnail']
        description =request.form['description']
        channel =request.form['channel']
        views =request.form['views']
        video  =request.form[' video ']
      
        conn = sql.connect('videos.db')
        conn.row_factory = sql.Row
        cur =conn.cursor()
        cur.execute('Insert into videos_table (NAME,THUMBNAILDP,THUMBNAIL,DESCRIPTION,CHANNEL,VIEWS,VIDEO) values(?,?,?,?,?)',(name,thumbnaildp,thumbnail,description,channel,views,video))
        conn.commit()
        return redirect(url_for('youtubehome'))
    return render_template('uplaod.html')



@app.route('/play/<id>')
def playfunc(id):
    conn =sql.connect('videos.db')
    conn.row_factory =sql.Row
    cur = conn.cursor()
    cur = cur.execute("Select * from videos_table where ID=? ",(id,))
    data_play  = cur.fetchone()
    return render_template('videoplayer.html',data_play=data_play)




@app.route('/li',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        name = request.form["name"]
        password = request.form["password"]
        conn = sql.connect('videos.db')
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute('select  *  from  login  where name=?',(name,))
        data = cur.fetchone()
        if data :
            if str(data['name']) == name  and  str(data['password']) == password:
                session['name'] = data['name']
                return redirect(url_for('home'))
        else:
            return'<h3>user is not exit </h3>'
    return render_template('form.html')

@app.route('/googleform')
def googleform():

    return render_template('gform.html')



@app.route('/adduser',methods =['POST','GET'])
def adduser():
    if request.method == 'POST':
        name = request.form["name"]
        password = request.form["password"]
        conn = sql.connect('videos.db')
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute('insert into login  (name,password) values(?,?)',(name,password))
        conn.commit()
        return redirect(url_for('youtubehome'))
    return render_template('adduser.html')



@app.route("/session")
def home():
    conn=sql.connect("videos.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("Select * from videos_table where EMAIL=?",(session["name"],))
    data=cur.fetchall()
    return render_template("session.html",data=data)

@app.route("/lo")
def logout():
    session.pop('name',None)
    return redirect(url_for('login'))



if __name__=='__main__':
    app.run(debug=True)











