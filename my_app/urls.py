from django.urls import include, path
from rest_framework import routers
from predict.views import PredictViewSet
from my_app.src import views

router = routers.DefaultRouter()
router.register(r'register', views.RegisterView, basename='register')
router.register(r'login', views.LoginView, basename='login')
router.register(r'predict', PredictViewSet, basename='predict')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]