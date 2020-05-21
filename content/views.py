import os
from django.http             import HttpResponse, StreamingHttpResponse, JsonResponse
from django.core.exceptions  import ObjectDoesNotExist
from django.views            import View
from pydub                   import AudioSegment
from django.db.models        import Sum
from .models                 import PlayList, PlayListGroup, Content
from user.models             import Teacher

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
