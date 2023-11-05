from django.conf.urls import url
from restaurant.views import RestaurantCreateUpdateProfileView, RestaurantBankDetailsCreateUpdateView, GetRestaurantsView, \
    GetRestaurantBankDetailsView, GetCuisinesView, GetMembershipsView

urlpatterns = [
    url(r'create_profile/$', RestaurantCreateUpdateProfileView.as_view()),
    url(r'update_profile/$', RestaurantCreateUpdateProfileView.as_view()),
    url(r'get_restaurants/$', GetRestaurantsView.as_view()),
    url(r'add_bank_details/?', RestaurantBankDetailsCreateUpdateView.as_view()),
    url(r'update_bank_details/?', RestaurantBankDetailsCreateUpdateView.as_view()),
    url(r'get_bank_details/?', GetRestaurantBankDetailsView.as_view()),
    url(r'get_cuisines/?', GetCuisinesView.as_view()),
    url(r'get_memberships/?', GetMembershipsView.as_view())
]