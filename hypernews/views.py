from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View


class MainPageView(View):
    def get(self, *args, **kwargs):
        return redirect('/news')