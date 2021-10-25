from flask import Flask,jsonify,make_response,Response,render_template, request
import src.cv_classifier as cls
from werkzeug.utils import secure_filename
import os

app = Flask('__name__', template_folder='template')

UPLOAD_FOLDER = 'uploaded_cv/'
IMAGE_FOLDER = os.path.join('static', 'image')
app.config['PLOT_FOLDER'] = IMAGE_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_post():
    
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
    #return 'file uploaded successfully'
    return render_template('download.html')

@app.route("/download")
def download():
    response=cls.main_method()
    
    #return jsonify(response) 

    resp = make_response(response.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route("/plot")
def plot():
    response=cls.main_method()
    cls.visualize(response)
    full_filename = os.path.join(app.config['PLOT_FOLDER'], 'short_listed.jpg')
    return render_template("home.html", user_image = full_filename)
   # return render_template('home.html', name = 'new_plot', 
                           #url ='C:/Users/subha/Data_Science/Deep Learning/NLP/CV classification/image/short_listed.jpg')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/search",methods=['POST'])
def search_result():
    text = request.form['Skill']
    print(text)
    df=cls.search_skills(text)
    
    # If you just want to get the vanilla structure: 
    df_html = df.describe().to_html()

    resp = make_response(render_template_string(df_html))
                         
    return resp
        

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)