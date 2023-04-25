import base64
import cv2
import io
import os
import imghdr
import tempfile
import numpy as np
from PIL import Image,ImageSequence
from moviepy.editor import VideoFileClip,ImageSequenceClip
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter

class count:
    def __init__(self,encode,model,fname):
        self.encode=encode
        self.model=model
        self.fname=fname
    def video_count(self):
        encode=base64.b64decode(self.encode.split("*")[1].split(",")[1])

        # Create an in-memory file-like object
        video_nparray = np.frombuffer(encode, dtype=np.uint8)
        # Open the video file with cv2.VideoCapture()
        temp_file_handle, temp_file_path = tempfile.mkstemp(suffix=".mp4")
        temp_file = open(temp_file_path, mode="wb")

        # Write the video frames to the temporary file
        temp_file.write(video_nparray)
        temp_file.close()
        cap = cv2.VideoCapture()
        cap.open(temp_file_path, apiPreference=cv2.CAP_ANY)
        #cap.write(video_nparray)
        if not cap.isOpened():
            print("Failed to open video file")
            exit()

        # Process the video frames using cv2 functions
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 255, 255)
        thickness = 2
        org = (50, 50)
        frameseq=[]
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process the frame as needed
            # ...
             # Write text on the frame
            
            result=self.model.predict(frame)
            img=cv2.putText(result[0].plot(), str(len(result[0].boxes)), org, font, font_scale, color, thickness, cv2.LINE_AA)
            frameseq.append(img)
           # cv2.imshow("frame", img)
            if cv2.waitKey(1) == ord("q"):
                break
        cap.release()
        width,height,_=frameseq[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.encode.split("*")[0],fourcc,30, (height,width))
        for frame in frameseq:
            out.write(frame)

        out.release()
        cv2.destroyAllWindows()
                # Read the video file into a bytes object
        with open(self.encode.split("*")[0], "rb") as video_file:
            video_data = video_file.read()

        # Convert the video data to a base64 string
        base64_data = base64.b64encode(video_data).decode("utf-8")
        videolist={}
        videolist[self.encode.split("*")[0]]=[base64_data]
        return videolist

                


