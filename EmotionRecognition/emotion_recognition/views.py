import json

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View


class MainPageView(View):
    template_name = 'emotion_recognition/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'emotion_recognition/index.html', context={})


def get_frame(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            JsonResponse({"is_succserful": False})
        print(data)
    return JsonResponse(data)


def get_mode(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            JsonResponse({"is_succserful": False})
    return JsonResponse(data)


def upload_video(request):
    if request.method == 'POST' and request.FILES:
        # получаем загруженный файл
        file = request.FILES['myfile1']
        fs = FileSystemStorage()
        # сохраняем на файловой системе
        filename = fs.save(file.name, file)
        # получение адреса по которому лежит файл
        file_url = fs.url(filename)
        print(filename)
        return HttpResponseRedirect('/')
