from django.shortcuts import render
from django.views import View


class MainPageView(View):
    template_name = 'emotion_recognition/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'emotion_recognition/index.html', context=context)
