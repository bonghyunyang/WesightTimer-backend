import jwt, bcrypt, json, re
from django.views                      import View
from django.http                       import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls                       import reverse
from .models                           import User
from wesight.settings                  import SECRET_KEY
from django.shortcuts import redirect

class SignUpView(View):

    VALIDATION_RULES = {
        'password' : lambda password: True if not re.search(r"^(?=.*[a-zA-Z])(?=.*[0-9])[0-9A-Za-z$&+,:;=?@#|'<>.^*()%!-]{6,50}$", password) else False
        }

    def post(self, request):
        try:
            data = json.loads(request.body)

            if len(data.keys()) < 3 :
                return HttpResponse(status = 400)

            for value in data.values():
                if value in "":
                    return HttpResponse(status=400)

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

        except ValueError:
            return HttpResponse(status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
                    user_name = user.full_name
                    user_email = user.email
                    return JsonResponse({'token_issued' : token.decode('utf-8'), 'name' : user_name, 'email' : user_email}, status = 200)

            return HttpResponse(status = 401)

        except KeyError:
            return JsonResponse({'message' : 'KeyError'}, status = 400)

        except ValueError:
            return HttpResponse(status = 400)

class TeacherView(View):
    def get(self, request):

        teacher_id = request.GET.get('teacher_id')

        teacher_info = Teacher.objects.get(id = teacher_id)

        teacher_detail = {
            'location': (teacher_info.location.city + ', ' + teacher_info.location.     country),
            'info': teacher_info.teacher_bio
         }
        return JsonResponse({'teacherDetail': teacher_detail}, status = 200)
