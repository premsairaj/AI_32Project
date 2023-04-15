from flask import redirect,render_template,request,Flask
from mode import model
import json
import mysql.connector
cnx = mysql.connector.connect(user='root', password='9493',
                              host='localhost', database='steelcount',autocommit=False)
cursor = cnx.cursor()
app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    if(request.method=='POST'):
        if(request.files['input'].filename.split(".")[-1]!='mp4'):
            md=model.yolov8model(request.form['b64'])
            dblist=md.bestmodel()
            for key,value in dblist.items():
                insert_query = "INSERT INTO inventory (filename, imread_array,total_rods_count) VALUES (%s, %s,%s)"
                cursor.execute(insert_query,(key,value[2],value[1]))
            cnx.commit()   
            cursor.close()
            cnx.close()
            return render_template('home.html',update=md.bestmodel())
        else:
            md=model.yolov8model(request.form['b64'])
            outlist=md.videoprediction()
            return render_template('home.html',update=outlist)


    else:
        return render_template('home.html')


if __name__=='__main__':
    app.run(debug=True)
   