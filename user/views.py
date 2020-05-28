import jwt
import bcrypt
import json
import re

from .models          import User
from wesight.settings import SECRET_KEY, app_id, app_secret

from django.views     import View
from django.http      import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls      import reverse
from django.shortcuts import redirect

class SignUpView(View):

    PASSWORD_RULE    = r"^(? = .*[a-zA-Z])(? = .*[0-9])[0-9A-Za-z$&+,:; = ?@#|'<>.^*()%!-]{6,50}$"
    VALIDATION_RULES = {
        'password'  : lambda password : not re.search(PASSWORD_RULE, password),
        'full_name' : lambda name     : len(name) > 0,
        'email'     : lambda email    : '@' in email
    }

    def post(self, request):
        try:
            data = json.loads(request.body)

            for value, validator in self.VALIDATION_RULES.items():
                if validator(data[value]):
                    return HttpResponse(status=400)

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'MESSAGE' : 'ALREADY_EXSIST'}, status = 401)

            User.objects.create(
                email     = data['email'],
                full_name = data['full_name'],
                password  = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            )
            
            return HttpResponse(status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE':'INVALIED_KEY'}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])
    
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token      = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
                    user_name  = user.full_name
                    user_email = user.email

                    return JsonResponse({
                        'token_issued' : token.decode('utf-8'),
                        'name'         : user_name,
                        'email'        : user_email
                    }, status = 200)

            return HttpResponse(status = 401)
        except KeyError:
            return JsonResponse({'message' : 'KeyError'}, status = 400)
