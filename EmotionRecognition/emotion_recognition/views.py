import json

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .emotion_recognition_services import State

state = State()


class MainPageView(View):
    template_name = 'emotion_recognition/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'emotion_recognition/index.html', context={})


def get_frame(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse(status=200, data={'message': 'all good'})
        except:
            JsonResponse(status=400, data={'message': 'error'})


def get_mode(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            state.set_mode(data)
            return JsonResponse(status=200, data={'message': 'all good'})
        except:
            JsonResponse(status=400, data={'message': 'error'})


def get_first_mode_result(request):
    if request.method == 'GET':
        if state.is_ready:
            JsonResponse(status=200, data={'emotion': state.final_video_emotion})
        else:
            JsonResponse(status=400, data={'emotion': state.final_video_emotion})

    else:
        JsonResponse(status=200, data={'error': 'not a get request'})


def upload_video(request):
    if request.method == 'POST' and request.FILES:
        # получаем загруженный файл
        file = request.FILES['myfile1']
        fs = FileSystemStorage()
        # сохраняем на файловой системе
        file_name = fs.save(file.name, file)
        # получение адреса по которому лежит файл
        file_url = fs.url(file_name)

        state.processing_first_mode(file_name, file_url)
        return HttpResponseRedirect('/')
