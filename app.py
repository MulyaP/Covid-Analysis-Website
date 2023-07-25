from flask import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import math
import os
from os.path import join, dirname, realpath
app = Flask(__name__)
app.secret_key = 'Mulya'

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER






@app.route('/', methods=['GET', 'POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    if request.method=='POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)

        global address
        address=[]
        def makeGraph(i):
            x1=[]
            for j in range(len(cities[i])):
                x1.append(j+1)
            x1 = np.array(x1)

            # print(x1)

            y1 = np.array(cities[i])
            # print(y1)
            plt.plot(x1,y1)
            plt.yticks(np.arange(min(y1), max(y1)+100, abs(y1[1]-y1[0])))
            s = "static/" + i + ".png"
            plt.savefig(s)
            address.append(s)
            plt.close()

        file = open(file_path,'r')
        csvreader = csv.reader(file)
        fields = next(csvreader)
        if fields[0]!='City' or fields[1]!='Cases':
            fail = "Wrong File Format"
            return render_template('Home.html',fail=fail)
        global cities
        cities = {}
        for row in csvreader:
            if row[0] in cities:
                cities[row[0]].append(int(row[1]))
            else:
                cities[row[0]] = []
                cities[row[0]].append(int(row[1]))

        
        global city
        city = list(cities.keys())

        # i = city[0]
        for i in city:
            makeGraph(i)

        global pred
        pred=[]

        for i in city:
            x1=[]
            for j in range(len(cities[i])):
                x1.append(j+1)
            x1 = np.array(x1)
            n = np.size(x1)
            y = np.array(cities[i])
            x = x1
            x = x.reshape(-1,1)

            model = LinearRegression()

            model.fit(x,y)

            predicted_price = model.predict([[x[n-1][0]+1]])

            pred.append(math.floor(predicted_price))
        return redirect('/data')

    return render_template('Home.html',fail='')

@app.route('/data', methods=['GET', 'POST'])
def index():
    return render_template('data.html',cities=cities)

@app.route('/Graph',methods=['GET','POST'])
def graph():

    return render_template('Graph.html',city=city,address=address)

@app.route('/Predict',methods=['GET','POST'])
def predict():
    return render_template('Predict.html',cities=cities,city=city,predict = pred)


if __name__ == '__main__':
    app.run(debug=True)