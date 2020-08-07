from django.urls import path
from .views import NewsDetailView, NewsListView, NewsCreateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', NewsListView.as_view(), name='articles-list'),
    path('/q=<q>', NewsListView.as_view(), name='articles-list'),
    path('<int:link>/', NewsDetailView.as_view(), name='article'),
    path('create/', NewsCreateView.as_view(), name='news-create'),

]
urlpatterns += static(settings.STATIC_URL)