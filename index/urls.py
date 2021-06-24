from django.urls import path
from . import views
from django.http import StreamingHttpResponse
from index.camera import VideoCamera,gen
urlpatterns = [
    path('', views.home,name='index_home'),
    path('uploadmanually/', views.manuallyupload,name='Upload_manually'),
    path('uploadimage/',views.uploadimage,name="uploadimage"),
    path('live/', views.live,name='Real_Time_Image'),
    path('live/video_feed/', lambda r: StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')),
    path('live/takeimage/', views.takeimage,name='Real_Time_Image'),
]
