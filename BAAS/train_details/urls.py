from django.conf.urls import url

from views import GetTrainLiveStatusForConsumer

urlpatterns = [
    url(r'^get_live_status/$', GetTrainLiveStatusForConsumer.as_view()),
]