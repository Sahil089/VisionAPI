from flask import*  
from function.mai import detect_web,logo_detection,objects_detection,label_detection
from google.cloud import vision,storage
import pandas as pd
import validators
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credintial/GCP_CRED.json"
storage_client = storage.Client()
bucket = storage_client.get_bucket('image-website-bucket')
blob = bucket.blob('image-data/DATA4.csv')
path = "gs://image-website-bucket/image-data/DATA4.csv"
df = pd.read_csv(path)

def product_description(img):
    obj=objects_detection(img)
    lab=label_detection(img)
    logo=logo_detection(img)
    final_data=obj+lab+logo
    if final_data=="Invalid Url":
        return final_data
    else:
        final_data= [item.lower() for item in final_data]
        print(final_data)
        final_pr_detail= df[df['Pname'].isin(final_data)]
        pr_data= final_pr_detail['URL']
        pr_name=final_pr_detail['Pname']
        print(pr_data)
        print(pr_name)
            
        return pr_data,pr_name

app = Flask(__name__)  
  
UPLOAD_FOLDER='uploads'
@app.route('/')   
def main():   
    return render_template("index.html")   
  
@app.route('/submit', methods = ['POST'])   
def submit():   
    if request.method == 'POST':
        url_img=request.form.get('url_link')
        if url_img.startswith('https://'):
            data,name=product_description(url_img)
        else:
            f = request.files['file']
            if f.filename == '':
                return "No selected file"   
            file_path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(file_path)
            data,name=product_description(file_path) 
        if data.empty:
            return render_template('no_data.html')
        else:
            final_result=zip(data,name)  
            return render_template("desc.html", data=final_result)

@app.route('/search', methods = ['POST']) 
def search():
    if request.method == 'POST':
        url_img=request.form.get('url_glob')
        if url_img.startswith('https://'):
            data=detect_web(url_img)
        else:
            f = request.files['file_glob']
            if f.filename == '':
                return "No selected file"   
            file_path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(file_path)
            data=detect_web(file_path) 
        return render_template("dec_glob.html", data=data)
