import requests
from rest_framework import generics
from .models import Job, Result
from .serializers import JobSerializer, ResultSerializer
from .authentication import ApiAuth
from .permissions import IsAdminOrManager


# Custom views using Django Rest Framework
class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = [ApiAuth]
    permission_classes = [IsAdminOrManager]

    # Associate the token user with the job (user added to request object thanks to authentication class)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user["username"])

        # add job to queue
        requests.post("http://127.0.0.1:7500/queues/jobs", json=serializer.data, headers={"Authorization": f"Bearer {self.request.auth}"})


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = [ApiAuth]
    permission_classes = [IsAdminOrManager]


class ResultList(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    authentication_classes = [ApiAuth]
    permission_classes = [IsAdminOrManager]


class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    authentication_classes = [ApiAuth]
    permission_classes = [IsAdminOrManager]
