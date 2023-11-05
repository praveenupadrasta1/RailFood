from django.conf.urls import url
from views import AddJourneyView, GetMyJourneys, GetJourney

urlpatterns = [
    url(r'^add_journey/$', AddJourneyView.as_view()),
    url(r'^get_journeys/$', GetMyJourneys.as_view()),
    url(r'^get_journey/$', GetJourney.as_view()),
]