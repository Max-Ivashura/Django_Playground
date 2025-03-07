import time

from django.http import HttpResponse
import gzip


class GZipMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.get('Content-Encoding', '') != 'gzip':
            response.content = gzip.compress(response.content)
            response['Content-Encoding'] = 'gzip'
        return response


class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(f"Запрос {request.path} обработан за {duration:.2f} сек.")
        return response


class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        blocked_ips = ['192.168.1.100']  # Добавьте свои IP
        if request.META.get('REMOTE_ADDR') in blocked_ips:
            return HttpResponse("Доступ заблокирован!")
        return self.get_response(request)
