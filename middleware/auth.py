from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
class Authmiddleware(MiddlewareMixin):
    def process_request(self,request):
        info_dict = request.session.get("info")
        if request.path_info == "/login/":
            return
        if info_dict:
            return
        return HttpResponse("Can't access")

    def process_response(self, request, response):
        return response

