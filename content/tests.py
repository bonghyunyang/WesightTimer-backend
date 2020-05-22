import json

from django.test import TestCase, Client

from user.models    import (
   PaymentStatus,
   Payment,
   Subscription,
   Location,
   TimeZone,
   SocialType,
   UserIntroduction,
   User,
   GenderType,
   Teacher
)
from content.models import (
   RootCategory,
   MiddleCategory,
   EndCategory,
   ActivityType,
   ContentType,
   Target,
   Content,
   PlayList,
   PlayListGroup
)

import unittest

class ContentAppTest(TestCase):

    def setUp(self):
        RootCategory.objects.create(
           id   = 1,
           name = "slow"
        )

        MiddleCategory.objects.create(
           id   = 1,
           name = "fast"
        )

        EndCategory.objects.create(
           id   = 1,
           name = "run"
        )

        PaymentStatus.objects.create(
           id     = 1,
           status = "super_plus"
        )

        Payment.objects.create(
           id           = 1,
           card         = "HYUNDAI",
           number       = "5554-5222-7795-9822",
           expire_date  = "2020/08/25"
        )

        Subscription.objects.create(
           id             = 1,
           campaign       = "lone",
           status_comment = "Trial Ends on",
           status_date    = "2020. 6. 10. 11:55:0",
           cycle          = "Yearly",
           started        = "2020/5/13",
           next_bill      = "2021/6/12",
           biling         = "Auto",
           next_cycle     = "59.99"
        )

        Location.objects.create(
            id       = 1,
            country  = "russia",
            city     = "moskva"
        )

        Location.objects.create(
            id       = 2,
            country  = "usa",
            city     = "LA"
        )

        TimeZone.objects.create(
            id   = 1,
            time = "go to home 25h"
        )

        SocialType.objects.create(
            id = 1,
            type = 'normal'
        )

        UserIntroduction.objects.create(
           id             = 1,
           location       = Location.objects.get(id=1),
           time_zone      = TimeZone.objects.get(id=1),
           website        = "www.wecode.com",
           tagline        = "fire codinging",
           introduction   = "fire coding now",
           profile_image  = "none"
        )

        User.objects.create(
           id                = 1,
           payment_status    = PaymentStatus.objects.get(id=1),
           payment           = Payment.objects.get(id=1),
           user_introduction = UserIntroduction.objects.get(id=1),
           social_login      = SocialType.objects.get(id=1),
           subscription      = Subscription.objects.get(id=1),
           email             = "aaa@aaa.com",
           full_name         = "aaa",
           password          = "qqqqqq111"
        )

        GenderType.objects.create(
           id   = 1,
           name = "4th"
        )
        
        Teacher.objects.create(
           id                 = 1,
           user               = User.objects.get(id=1),
           gender             = GenderType.objects.get(id=1),
           location           = Location.objects.get(id=2),
           name               = "ki",
           unique_name        = "kiki",
           teacher_bio        = "no no no",
           facebook           = "face.com",
           twitter            = "twi.com",
           linked_in          = "link.com",
           email              = "aaa@aaa.com",
           facebook_messenger = "faceme.com",
           teacher_img        = "none"
        )

        ActivityType.objects.create(
           id   = 1,
           name = "run"
        )

        ContentType.objects.create(
           id   = 1,
           name = "medi"
        )

        Target.objects.create(
           id   = 1,
           name = "you"
        )

        Content.objects.create(
           id            = 1,
           teacher       = Teacher.objects.get(id=1),
           content_type  = ContentType.objects.get(id=1),
           activity_type = ActivityType.objects.get(id=1),
           target        = Target.objects.get(id=1),
           title         = "title",
           description   = "none",
           image_url     = "none",
           running_time  = "10:10",
           file_source   = "/home/shoo/real_project/WesightTimer-backend/mp3/1.mp3",
           course_img    = "222"
        )

        Content.objects.create(
           id            = 2,
           teacher       = Teacher.objects.get(id=1),
           content_type  = ContentType.objects.get(id=1),
           activity_type = ActivityType.objects.get(id=1),
           target        = Target.objects.get(id=1),
           title         = "title",
           description   = "none",
           image_url     = "none",
           running_time  = "10:10",
           file_source   = "/home/shoo/real_project/WesightTimer-backend/mp3/2.mp3",
           course_img    = "222"
        )

        Content.objects.create(
           id            = 3, 
           teacher       = Teacher.objects.get(id=1),
           content_type  = ContentType.objects.get(id=1),
           activity_type = ActivityType.objects.get(id=1),
           target        = Target.objects.get(id=1),
           title         = "title",
           description   = "none",
           image_url     = "none",
           running_time  = "10:10",
           file_source   = "/home/shoo/real_project/WesightTimer-backend/mp3/3.mp3",
           course_img    = "222"
        )

        PlayList.objects.create(
           id       = 1,
           teacher  = Teacher.objects.get(id=1),
           title    = "playlist",
           describe = "playplay",
           pick     = True
        )

        PlayListGroup.objects.create(
           id         = 1,
           play_list  = PlayList.objects.get(id=1),
           content    = Content.objects.get(id=1)
        )

        PlayListGroup.objects.create(
           id         = 2,
           play_list  = PlayList.objects.get(id=1),
           content    = Content.objects.get(id=2)
        )

        PlayListGroup.objects.create(
           id         = 3,
           play_list  = PlayList.objects.get(id=1),
           content    = Content.objects.get(id=3)
        )

    def tearDown(self):
        RootCategory.objects.all().delete(),
        MiddleCategory.objects.all().delete()
        EndCategory.objects.all().delete()
        PaymentStatus.objects.all().delete()
        Payment.objects.all().delete()
        Subscription.objects.all().delete()
        Location.objects.all().delete()
        TimeZone.objects.all().delete()
        UserIntroduction.objects.all().delete()
        User.objects.all().delete()
        GenderType.objects.all().delete()
        Teacher.objects.all().delete()
        ActivityType.objects.all().delete()
        ContentType.objects.all().delete()
        Target.objects.all().delete()
        Content.objects.all().delete()
        PlayList.objects.all().delete()
        PlayListGroup.objects.all().delete()

    def test_play_list_main_bad_request(self):
        client   = Client()
        response = client.get('/content/playlistmain?offset=asdf&limit=asdf')
        self.assertEqual(response.status_code, 400)

    def test_play_list_main_range_over_request(self):
        client   = Client()
        response = client.get('/content/playlistmain?offset=-1&limit=1000000')
        self.assertEqual(response.status_code, 400)

    def test_play_list_info_does_not_exsist(self):
        client   = Client()
        response = client.get('/content/playlistinfo/-11111')
        self.assertEqual(response.status_code, 404)

    def test_play_list_main_success(self):
        client  = Client()
        response = client.get('/content/playlistmain?offset=0&limit=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            "staff_pick": [{"playlist_id": 1, "title": "playlist", "teacher": "kiki", "discribe": "playplay", "image_url": ["none", "none", "none"]}],

            "play_list": [
                {
                    "playlist_id": 1,
                    "title": "playlist",
                    "teacher": "kiki",
                    "discribe": "playplay",
                    "image_url": ["none", "none", "none"]
                }
            ]
        }
        )

    def test_play_list_info_success_response(self):
        client   = Client()
        response = client.get('/content/playlistinfo/1')
        self.assertEqual(response.json(),
        {
            "playlist": {
                "playtime": "0:30:30",
                "title": "playlist",
                "teacher": "kiki",
                "describe": "playplay"
            },
            "content": [
                {
                    "id": 1,
                    "title":"title",
                    "teacher": "kiki",
                    "playtime": "10:10",
                    "imgurl": "none"
                },
                {
                    "id": 2,
                    "title":"title",
                    "teacher": "kiki",
                    "playtime": "10:10",
                    "imgurl": "none"
                },
                {
                    "id": 3,
                    "title":"title",
                    "teacher": "kiki",
                    "playtime": "10:10",
                    "imgurl": "none"
                },
            ]
        }
        )

    def test_contentplay_bad_request(self):
        client   =  Client()
        response = client.get('/content/playcontent/-111')
        self.assertEqual(response.status_code, 404)

    def test_contentplay_dose_not_exsist(self):
        client   = Client()
        response = client.get('/content/playcontent/99999999999')
        self.assertEqual(response.status_code, 404)

    def test_contentplay_success_response(self):
        client   = Client()
        response = client.get('/content/playcontent/3')
        self.assertEqual(response.get('Content-Type'), 'audio/mp3')
        self.assertEqual(response.status_code, 200)