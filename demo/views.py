import json

from celery import result
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response

from rest_framework.decorators import action

from demo.models import Demo
from demo.serializers import DemoSerializer

from rest_framework import viewsets, status
from rest_framework.views import APIView

from demo.tasks import add, startMq
from demo.mq.Receiver import AMQPConsuming
from demo.mq.Producer import AMQPProducer

# startMq.delay()
t = AMQPConsuming()
t.start()

producer = AMQPProducer()
print("start======")
# rest framwork寫法
class DemoViewSet(viewsets.ModelViewSet):
    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    queryset = Demo.objects.all()
    serializer_class = DemoSerializer
    http_method_names = ['get', 'post']

    @action(detail=False, methods=['get'])
    def hello(self, request):
        return Response({'status': 'hello'})

    # http://127.0.0.1:8000/rest/demo/run_data/
    @action(detail=False, methods=['post'])
    def run_data(self, request):
        print("data: ", request.data)
        return Response({'status': 'password set '})
        # return Response({'status': 'password set'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def test_task(self, request):
        ar = add.delay(1, 2)
        return HttpResponse(f'已經執行celery的add任務呼叫,task_id:{ar.id}')

    @action(detail=False, methods=['get'])
    def q_msg(self, request):
        producer.send()
        return Response({'status': 'ok'})

    @action(detail=False, methods=['post'])
    def q_task(self, request):
        print("data: ", request.body)
        print("data: ", type(request.body))
        data = json.loads(request.body)
        task_id = data['task_id']
        print("task_id:", task_id)
        ar = result.AsyncResult(task_id)
        print(ar.result)
        if ar.ready():
            return JsonResponse({"status": ar.state, "result": ar.get()})
        else:
            return JsonResponse({"status": ar.state, "result": ""})


# old 寫法
class DemoComponent(APIView):
    def get(self, request):
        return Response({'response': 'hello world'})
