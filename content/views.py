import os
import mimetypes

from user.models import Teacher
from .models     import (
    PlayList,
    PlayListGroup,
    Content,
    ContentReview,
    MiddleContentTag
)

from django.http             import HttpResponse, StreamingHttpResponse, JsonResponse
from django.core.exceptions  import ObjectDoesNotExist
from django.views            import View
from django.db.models        import Sum, Avg, F
from pydub                   import AudioSegment
from datetime                import datetime

class PlayListInfoView(View):

    def get(self, request, play_list_id):
        try:
            list_info       = PlayList.objects.get(id = play_list_id).prefetch_related('play_list_group_set')
            play_list_group = list_info.play_list_group_set
            play_time       = sum([p.content.get_play_time_as_second for p in play_list_group])

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

            staff_pick = [{
                "play_list_id" : pick.id,
                "title"        : pick.title,
                "teacher"      : pick.teacher.unique_name,
                "discribe"     : pick.describe,
                "image_url"    : list(pick.playlistgroup_set.values_list(img_url, flat=True))[:image_count]
            }for pick in picks]

            play_list = [{
                "play_list_id" : playlist.id,
                "title"        : playlist.title,
                "teacher"      : playlist.teacher.unique_name,
                "discribe"     : playlist.describe,
                "image_url"    : list(playlist.playlistgroup_set.values_list(img_url, flat=True))[:image_count]
             } for playlist in playlists[offset : offset + limit]]

            return JsonResponse({"staff_pick" : staff_pick, "play_list" : play_list}, status = 200)
        except ValueError:
            return HttpResponse(status = 400)

class RangeFileWrapper (object):
    def __init__(self, filelike, blksize, resume, length=None):
        self.filelike  = filelike
        self.remaining = length - resume
        self.blksize   = blksize
        data           = self.filelike.seek(resume)

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
            source  = Content.objects.get(id = content_id).file_source
            name    = os.path.basename(source)
            size    = os.path.getsize(source)
            content = AudioSegment.from_mp3(source)
            length  = int(len(content) / 1000)
            chunk   = int(size / length)

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
        content_id = request.GET.get('content_id')

        if not content_id:
            return HttpResponse(status = 400)

        # 다 연결 되지않았나?
        rating   = ContentReview.objects.filter(id = content_id)
        contentt = Content.objects.get(id = content_id)
        rate_is  = ContentReview.objects.select_related('content', 'content_rating').filter(id = content_id).aggregate(Avg('content_rating__rating'))['content_rating__rating__avg']
        
        music_info = {
            "playtime"         : contentt.running_time,
            "title"            : contentt.title,
            "teacher"          : contentt.teacher.unique_name,
            "rate"             : str(rate_is),
            "type"             : contentt.content_type.name,
            "activity"         : contentt.activity_type.name,
            "suitableTarget"   : contentt.target.name,
            "musicDescription" : contentt.description,
            "player_image"     : contentt.image_url
         }

        tags          = MiddleContentTag.objects.filter(content = content_id)
        category_Info = [tag.middle_category.name for tag in tags]

        return JsonResponse({"music_info" : musicInfo, "category_info" : category_info}, status = 200)

class StressReviewView(View):
    def get(self, request, content_id):s
        content_rates = (
            ContentReview
            .objects
            .select_related('content', 'user', 'content_rating')
            .filter(content = content_id)
            .aggregate(Avg('content_rating__rating'))
        )

        review_element = (
            ContentReview
            .objects
            .select_related('user', 'content')
            .all()
            .annotate(
                con_id        = F('content_id__id'),
                username      = F('user_id__full_name'),
                rating        = F('content_rating_id__rating'),
                reviewContent = F('review')
            ).values(
                'con_id', 
                'username', 
                'rating', 
                'reviewContent', 
                'write_date'
            )
        )
        
        return JsonResponse({'review': list(content_rates), 'reviews': list(review_element)}, status = 200)

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
