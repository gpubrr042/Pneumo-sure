from .headers import *
import numpy.core.multiarray
import cv2
from sanic import response
import asyncio


# PRevents the application from caching the inputs to the browser
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# Aclass that defines,initializes and generates input from the device camera
class Camera(object):
  def __init__(self):
    self.cap = cv2.VideoCapture(0)

  def get_frame(self):
    ret, frame = self.cap.read()
    ret, jpeg = cv2.imencode('.jpeg', frame)
    return jpeg.tobytes()
    
async def gen(camera, response):
    """Video streaming generator function."""
    loop = asyncio.get_event_loop()
    while True:
        frame = await loop.run_in_executor(None, camera.get_frame)
        response.write(b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        await asyncio.sleep(1.0/FPS)


 
@app.route('/', methods=['GET','POST'])
def home():
    return render_template("home.html")

def redirecting():
    return render_template("capture.html")
 

@app.route('/capture')
def capture():
    return render_template("capture.html")




# Route triggered whn the upload is successful
@app.route('/result', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(os.path.join(app.root_path, "static","test.jpeg")) 

        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

        with open(app.root_path + "/static/test.jpeg", "rb") as image_contents:
            results = predictor.classify_image(
                projectId, publish_iteration_name, image_contents.read())
            result=""
            for prediction in results.predictions:
                result += "\t\t\n" + prediction.tag_name + " : {0:.2f}% ".format(prediction.probability * 100)

        return render_template("result.html", result = result)  


# Route triggered whn the Live capture is successful
@app.route('/result-capture', methods = ['POST'])  
def success1():  
    if request.method == 'POST':  
        ret,img = cv2.VideoCapture(0).read()
        cv2.imwrite(os.path.join(app.root_path, "static","test1.jpeg"),img)
        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

        with open(app.root_path + "/static/test1.jpeg", "rb") as image_contents:
            results = predictor.classify_image(
                projectId, publish_iteration_name, image_contents.read())
            result=""
            for prediction in results.predictions:
                result += "\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100)

        return render_template("result-capture.html",result = result)  



