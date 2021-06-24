from django.shortcuts import render,redirect
from django.http import StreamingHttpResponse
from index.camera import VideoCamera
from django.core.files.storage import FileSystemStorage
import cv2
import numpy
from index.Graphical_Visualisation import Emotion_Analysis
def home(request):
    return render(request,'index/start.html')
def manuallyupload(request):
    return render(request,'index/uploadmanually.html')
def live(request):
    return render(request,'index/live.html')
def takeimage(request):
    v = VideoCamera()
    _, frame = v.video.read()
    save_to = "./index/static/"
    cv2.imwrite(save_to + "capture" + ".jpg", frame)
    result = Emotion_Analysis("capture.jpg")
    if(len(result)==1):
        return render(request,'index/error.html')
    return render(request,'index/result.html')
import os
def uploadimage(request):
    if request.method=='POST':
        doc = request.FILES
        if doc['myfile']:
            save_to = "./index/static/"
            img = cv2.imdecode(numpy.fromstring(doc['myfile'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
            cv2.imwrite(save_to + "capture.jpg", img)
            result = Emotion_Analysis("capture.jpg")
            if(len(result)==1):
                return render(request,'index/error.html')
            return render(request,'index/result.html')
