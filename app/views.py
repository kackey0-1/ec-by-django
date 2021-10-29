from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health(self, *args, **kwargs):
    status_code = 200
    results = {'status': 'HOGEHOGE'}
    return Response(results, status=status_code)
