from flask import Flask,request,render_template 
import numpy as np
import pickle

app=Flask(__name__)

model=pickle.load(open('model.pkl','rb'))
sc=pickle.load(open('sc.pkl','rb'))
state_value=pickle.load(open('state.pkl','rb'))

#response=['CA','80','4','2','0','0','55000','55000','50000','0','0','1']


@app.route('/predict',methods=['POST'])
def predict():
    response=[x for x in request.form.values()]
    a=float(state_value.loc[state_value.State==response[0],'Value'])
    response[0]=a

    response=np.array(response).reshape(1,-1)
    response=sc.transform(response)
    pred=model.predict(response)
    
    if pred==1:
        return render_template("pred.html",predicted="High chance to default !!!")
    return render_template("pred.html",predicted="Less chance to default")

@app.route('/')
def home():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)
    
