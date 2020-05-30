import os, mimetypes
from django.http             import HttpResponse, StreamingHttpResponse, JsonResponse
from django.core.exceptions  import ObjectDoesNotExist
from django.views            import View
from pydub                   import AudioSegment
from django.db.models        import Avg
from user.models             import Teacher
from .models                 import (
    PlayList,
    PlayListGroup,
    Content,
    ContentReview,
    MiddleContentTag
)

class PlayLisInfoView(View):
    def get(self, request, playlist_id):
        try:
            list_info      = PlayList.objects.get(id = playlist_id)
            contents       = PlayListGroup.objects.select_related('play_list','content').filter(play_list = playlist_id)
            all_play_time  = Content.objects.prefetch_related('playlistgroup_set').filter(playlistgroup__play_list = playlist_id).values('running_time')

            hour   = 0
            min    = 0
            second = 0

            for time in all_play_time:
                time_temp  = time['running_time'].split(':')
                if len(time_temp) == 2:
                    min    += int(time_temp[0])
                    second += int(time_temp[1])

            min       = min + int(second/60)
            second    = int(second % 60)
            hour      = hour + int(min/60)
            min       = int(min % 60)
            play_time = f"{hour}:{min}:{second}"


            playlist_info = {
                "playtime" : play_time,
                "title"    : list_info.title,
                "teacher"  : list_info.teacher.unique_name,
                "describe" : list_info.describe
            }

            contents_info = [{
                "id"       : content.content.id,
                "title"    : content.content.title,
                "teacher"  : content.content.teacher.unique_name,
                "playtime" : content.content.running_time,
                "imgurl"   : content.content.image_url
                }for content in contents]

            return JsonResponse({"playlist" : playlist_info, "content" : contents_info}, status = 200)

        except ObjectDoesNotExist:
            return HttpResponse(status = 404)

class PlayListMain(View):
    def get(self, request):
        try:
            offset      = int(request.GET.get('offset', 0))
            limit       = int(request.GET.get('limit', 10))
            image_count = int(request.GET.get('img', 3))

            all_play_list  = PlayList.objects.prefetch_related('playlistgroup_set')
            picks          = all_play_list.filter(pick = True)
            playlists      = all_play_list.order_by('-id')
            img_url        = 'content__image_url'

            if offset < 0 or offset > len(playlists):
                return HttpResponse(status = 400)

            if limit < 0 or limit >len(playlists):
                return HttpResponse(status = 400)

            staff_pick = [{
                "playlist_id" : pick.id,
                "title"       : pick.title,
                "teacher"     : pick.teacher.unique_name,
                "discribe"    : pick.describe,
                "image_url"   : list(pick.playlistgroup_set.values_list(img_url, flat=True))[:image_count]
             }for pick in picks]

            play_list = [{
                "playlist_id" : playlist.id,
                "title"       : playlist.title,
                "teacher"     : playlist.teacher.unique_name,
                "discribe"    : playlist.describe,
                "image_url"   : list(playlist.playlistgroup_set.values_list(img_url, flat=True))[:image_count]
             }for playlist in playlists[offset : offset + limit]]

            return JsonResponse({"staff_pick" : staff_pick, "play_list" : play_list}, status = 200)

        except ValueError:
            return HttpResponse(status = 400)

class RangeFileWrapper (object):
    def __init__(self, filelike, blksize, resume, length=None):
        self.filelike = filelike
        self.remaining = length - resume
        self.blksize = blksize
        data = self.filelike.seek(resume)

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data

class ContentPlay(View):
    def get(self, request, content_id):
        try:
            second  = int(request.GET.get('second', 0))
            content  = Content.objects.get(id = content_id)
            source  = content.file_source
            name    = os.path.basename(source)
            size    = os.path.getsize(source)
            content = AudioSegment.from_mp3(source)
            length  = int(len(content) / 1000)
            chunk   = int(size / length)

            if second < 0 or second > length:
                return HttpResponse(status = 400)

            content_type, encoding = mimetypes.guess_type(source)
            content_type = content_type or 'application/octet-stream'

            resp = StreamingHttpResponse(RangeFileWrapper(open(source, 'rb'), chunk * 1, chunk * second, size), status=200, content_type = 'audio/mp3')
            resp["Cache-Control"] = "no-cache"
            resp["Accept-Ranges"] = "bytes"
            resp["Content-Disposition"] = f"attachment; filename={name}"

            return resp

        except ObjectDoesNotExist:
            return HttpResponse(status = 404)

class StressPlaylistView(View):
    def get(self, request):

        content_id = request.GET.get('content_id', None)

        if content_id == None:
            return HttpResponse(status = 400)

        rating   = ContentReview.objects.filter(id = content_id)
        contentt = Content.objects.get(id = content_id)
        rate_is  = ContentReview.objects.select_related('content', 'content_rating').filter(id = content_id).aggregate(Avg('content_rating__rating'))['content_rating__rating__avg']
        
        musicInfo = {
            "playtime": contentt.running_time,
            "title": contentt.title,
            "teacher": contentt.teacher.unique_name,
            "rate": str(rate_is),
            "type": contentt.content_type.name,
            "activity": contentt.activity_type.name,
            "suitableTarget": contentt.target.name,
            "musicDescription": contentt.description,
            "player_image": contentt.image_url
         }

        tag1 = MiddleContentTag.objects.filter(content = content_id)

        categoryInfo = []

        for i in tag1:
            categoryInfo.append(i.middle_category.name)

        print(categoryInfo)

        return JsonResponse({"musicInfo" : musicInfo, "categoryInfo" : categoryInfo}, status = 200)

class StressReviewView(View):
    def get(self, request):
        
        content_id = request.GET.get('content_id', None)

        if content_id == None:
            return HttpResponse(status = 400)                                   

        content_rate = ContentReview.objects.select_related('content', 'user', 'content_rating').filter(id = content_id).aggregate(Avg('content_rating__rating'))
        content_is = content_rate.values()
        
        review_element = ContentReview.objects.select_related('user', 'content').all().annotate(con_id=F('content_id__id'), username=F('user_id__full_name'), rating=F('content_rating_id__rating'), reviewContent=F('review')).values('con_id', 'username', 'rating', 'reviewContent', 'write_date')
        
        return JsonResponse({'review': list(content_is), 'reviews': list(review_element)}, status = 200)
        return JsonResponse({'message':'review_does_not_exist'}, status = 400)


class MainView(View):
    def get(self, request):

        offset  = int(request.GET.get('offset', 0))
        limit   = int(request.GET.get('limit', 10))

        main_elements = Content.objects.select_related('teacher').order_by('id')

        main_content = [{
                "scoretext"   : ContentReview.objects.select_related('content', 'content_rating').filter(id = content.id).aggregate(Avg('content_rating__rating'))['content_rating__rating__avg'],
                "title"       : content.title,
                "description" : content.teacher.name,
                "time"        : str(content.running_time).split(':')[0] + ' ' + 'min',
                "imageURL"    : content.image_url
                } for content in main_elements[offset:offset+limit]]

        return JsonResponse({'Rolldata' : list(main_content)}, status = 200)