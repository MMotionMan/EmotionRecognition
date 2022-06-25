from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from .views import MainPageView, get_frame, upload_video, get_mode, get_first_mode_result

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('send_frame/', csrf_exempt(get_frame)),
    path('upload_video/', upload_video, name='upload_video'),
    path('send_mode/', csrf_exempt(get_mode)),
    path('get_first_mode_result/', get_first_mode_result)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)