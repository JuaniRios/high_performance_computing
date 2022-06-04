from django.contrib import admin
from django.urls import path
from .views import JobList, JobDetail, ResultList, ResultDetail

urlpatterns = [
    path("jobs", JobList.as_view(), name="job-list"),
    path("jobs/<int:pk>", JobDetail.as_view(), name="job-detail"),
    path("results", ResultList.as_view(), name="result-list"),
    path("results/<int:pk>", ResultDetail.as_view(), name="result-detail"),
]