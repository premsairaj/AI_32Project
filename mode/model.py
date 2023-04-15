from ultralytics import YOLO
import cv2
from moviepy.editor import VideoFileClip
import base64
import io
import os
import tempfile
import numpy as np
from werkzeug.utils import secure_filename
import time
class yolov8model:
    def __init__(self,input):
        self.input=input  
    def bestmodel(self,modelpath="E:\\AI_32Project\\model_kaggle\\kaggle\\working\\runs\\detect\\train\\weights\\best.pt"):
        imageslist={}
        update_list={}
        try:
            for i in self.input.split("  "):
                imageslist[i.split("*")[0]]=i.split("*")[1].split(",")[1]
                if i.split("*")[0].split(".")[-1] in ["jpg","png","jpeg"]:
                    image_bytes = base64.b64decode(imageslist[i.split("*")[0]])
                    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
                    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                    model=YOLO(modelpath)
                    result=model.predict(source=image,save=True)
                    buffer = cv2.imencode('.jpg', result[0].plot())[1]
                    image_bytes = buffer.tobytes()
                    # Encode the byte string to a Base64 string
                    base64_str = base64.b64encode(image_bytes).decode('utf-8')
                    update_list[i.split("*")[0]]=[base64_str,str(len(result[0].boxes)),str(result[0].plot())]
                   
        except IndexError as ie:
            pass
        return update_list  
    def videoprediction(self,modelpath="E:\\AI_32Project\\model_kaggle\\kaggle\\working\\runs\\detect\\train\\weights\\best.pt"):
        videodetails={}
        dir_path = "E:\\AI_32Project\\flask\\runs\\detect"

        # get list of all filenames in the directory
        all_files = os.listdir(dir_path)

        # get the most recently added filename based on modification time
        recent_file = max(all_files, key=lambda x: os.path.getmtime(os.path.join(dir_path, x)))

        filename=self.input.split("*")[0]
        decodevideo=base64.b64decode(self.input.split("*")[1].split(",")[1])
        with open(filename, 'wb') as f:
             f.write(decodevideo)
             f.close()
        model=YOLO(modelpath)
        result=model.predict(source=os.getcwd()+"\\"+filename,save=True)
        with open(dir_path+"\\"+recent_file+"\\"+filename, 'rb') as fp:
            videodetails[self.input.split("*")[0]] =[base64.b64encode(fp.read()).decode('utf-8')]
        return videodetails


