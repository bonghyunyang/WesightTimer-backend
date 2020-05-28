from django.urls import path

from .views import (
    PlayLisInfoView,
    PlayListMain,
    ContentPlay,
    StressReviewView,
    StressPlaylistView,
    MainView
)

urlpatterns = [
    path('/playlistinfo/<int:playlist_id>' , PlayListInfoView.as_view())  ,
    path('/playlist'                       , PlayListMainView.as_view())  ,
    path('/playcontent/<int:content_id>'   , ContentPlayView.as_view())   ,
    path('/detail'                         , StressPlaylistView.as_view()),
    path('/stressreview'                   , StressReviewView.as_view())  ,
    path('/main'                           , MainView.as_view())
]
