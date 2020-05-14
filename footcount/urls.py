from django.contrib import admin
from django.urls import path, include
from .views import (
    AnalyzeClass,
    HomeClass,
    CongestionHoursClass,
    ForecastClass,
    EmployeeRegClass,
    IndexClass,
    CountingClass,
    # test
)
from . import views


urlpatterns = [
    path('classification', views.classification, name="classification"),
    path('time_spent', views.time_spent, name="time_spent"),

    path('', IndexClass.as_view(), name="Home"),
    path('employee_reg', EmployeeRegClass.as_view(), name="employee_reg"),
    path('visitors_reg', views.visitors_reg, name="visitors_reg"),
    path('analyze', AnalyzeClass.as_view(), name="analyze"),
    path('live1', views.live1, name="live1"),
    path('live_stream/', views.indexscreen, name="indexscreen"),
    path('home', HomeClass.as_view(), name="home"),
    path('counting', CountingClass.as_view(), name="footcount"),
    path('forecast', ForecastClass.as_view(), name="forecast"),
    path('congestion_hours', CongestionHoursClass.as_view(), name="congestion_hours"),
    path('^(?P<stream_path>(.*?))/$', views.live, name="live"),
    # path('rest_api', include(router.urls))
    path('accounts/', include('django.contrib.auth.urls')),
]
