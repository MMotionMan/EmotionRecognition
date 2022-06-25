import json

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .emotion_recognition_services import State

from multiprocessing import Process

state = State()


class MainPageView(View):
    template_name = 'emotion_recognition/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'emotion_recognition/index.html', context={})


def get_frame(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            return JsonResponse(status=200, data={'message': 'all good'})
        except:
            JsonResponse(status=400, data={'message': 'error'})


def get_mode(request):
    print(request)
    print(request.method)
    if request.method == 'POST':
        try:
            print(request.body)
            data = json.loads(request.body)
            print(data)
            state.set_mode(data)
            return JsonResponse(status=200, data={'message': 'all good'})
        except BaseException as a:
            return JsonResponse(status=400, data={'message': 'error'})


def get_first_mode_result(request):
    error_json = 'error'

    if request.method == 'GET':
        if state.is_ready:
            data = state.final_video_emotion
            return HttpResponse(data, content_type='application/json')
        else:
            return HttpResponse(error_json, content_type='application/json')
    else:
        return HttpResponse(error_json, content_type='application/json')


def upload_video(request):
    success_json = {"is_success": "true"}
    error_json = {"is_success": "false"}
    if request.method == 'POST' and request.FILES:
        # получаем загруженный файл
        file = request.FILES['myfile1']
        fs = FileSystemStorage()
        # сохраняем на файловой системе
        file_name = fs.save(file.name, file)
        state.file_name = file_name

        p = Process(target=state.processing_first_mode, args=(state,))
        p.start()

        return redirect('/')

    return HttpResponse(error_json, content_type='application/json')


def set_next_frame(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            state.q_frames.append(data['image'])
            return JsonResponse(status=200, data={'message': 'all good'})
        except:
            JsonResponse(status=400, data={'message': 'error'})

    return HttpResponse({"is_success": "false"}, content_type='application/json')


def get_next_emotion(request):
    error_json = {"is_success": "false"}
    if request.method == 'GET' and state.q_emotions:
        # получаем загруженный файл
        success_json = {"is_success": "true", "emotion": state.q_emotions.popleft()}
        print("JSON = {}" % success_json)
        return HttpResponse(success_json, content_type='application/json')

    return HttpResponse(error_json, content_type='application/json')
