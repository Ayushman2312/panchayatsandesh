from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('about-us', AboutUsView.as_view(), name="about-us"),
    path('gallery', GalleryView.as_view(), name="gallery"),
    path('panchayat-reporter', PanchayatReporter.as_view(), name="panchayat-reporter"),
    path('upcoming-events', UpcomingEventsView.as_view(), name="upcoming-events"),
    path('team', TeamView.as_view(), name="team"),
    path('news/<str:news_title>/', NewsDetailView.as_view(), name='news-detail'),
    path('subscribe', SubscribeView.as_view(), name='subscribe'),
    path('categories', CategoryView.as_view(), name='categories'),
    path('categories/<str:category_name>/', CategoryNewsView.as_view(), name='category_articles'),
    path("live", LivestreamView.as_view(), name="livestream"),
    path('donate/', DonationView.as_view(), name='donation'),
    path('event/<slug:slug>/', UpcomingEventsView.as_view(), name='event_detail'),
    path('event/<slug:slug>/register/',RegistrationFormView.as_view(), name='event_register'),
    path('registration-success/', registration_success, name='event_registration_success'), 
    path('categories/<slug:category_slug>/<slug:news_slug>', CategoryNewsDetailView.as_view(), name='category_news_detail'),
    path('comment/<str:article_id>/', CommentView.as_view(), name='comment')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
