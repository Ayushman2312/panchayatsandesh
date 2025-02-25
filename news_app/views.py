from typing import Any
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.views import View


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_hot_news = HotNews.objects.order_by('-created_at').first()
        trending_news = TrendingNews.objects.order_by('-created_at')[:4]
        last_news = LastNews.objects.order_by('-created_at')[:4]
        breaking_news = BreakingNews.objects.order_by('-created_at')[:2]
        bb = BreakingNews.objects.order_by('-created_at')[:1]
        breakingnews = BreakingNews.objects.all()
        context["bb"] = bb
        context["breakingnews"] = breakingnews
        context["latest_hot_news"] = latest_hot_news
        context["trending_news"] = trending_news
        context["breaking_news"] = breaking_news
        context["last_news"] = last_news
        return context
    
class CategoryView(TemplateView):
    template_name = "categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context["category"] = category
        return context
    

class AboutUsView(TemplateView):
    template_name = 'about-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TeamView(TemplateView):
    template_name = 'team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        return context
    
class UpcomingEventsView(TemplateView):
    template_name = 'upcoming-events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = UpcomingEvents.objects.all()
        # If you need to display a specific event's details based on a slug:
        if 'slug' in self.kwargs:
            context['event'] = get_object_or_404(UpcomingEvents, slug=self.kwargs['slug'])
        return context
    
class RegistrationFormView(TemplateView):
    template_name = 'register_event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(UpcomingEvents, slug=self.kwargs['slug'])
        return context

    def post(self, request, *args, **kwargs):
        event = get_object_or_404(UpcomingEvents, slug=self.kwargs['slug'])
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Check if the user (identified by email) is already registered for this event
        if EventRegistration.objects.filter(event=event, email=email).exists():
            messages.error(request, "You are already registered for this event")
            return redirect('event_register', slug=event.slug)
        else:
            register = EventRegistration(
                event=event,
                name=name,
                email=email,
            )
            register.save()
        # Increment the registration count
        event.no_of_registers += 1
        event.save()

        return redirect('event_registration_success') 
    

def registration_success(request):
    return render(request, 'registration_success.html') 
    
class GalleryView(TemplateView):
    template_name = 'gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gallery = GalleryImages.objects.all()
        context["gallery"] = gallery
        return context
    
class PanchayatReporter(TemplateView):
    template_name = 'panchayat-reporter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewsDetailView(TemplateView):
    template_name = "news-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_title = self.kwargs["news_title"]

        if HotNews.objects.filter(title=news_title).exists():
            news = get_object_or_404(HotNews, title=news_title)
            context["news"] = news
            context["category"] = "Hot News"

        elif TrendingNews.objects.filter(title=news_title).exists():
            news = get_object_or_404(TrendingNews, title=news_title)
            context["news"] = news
            context["category"] = "Trending News"

        elif BreakingNews.objects.filter(title=news_title).exists():
            news = get_object_or_404(BreakingNews, title=news_title)
            context["news"] = news
            context["category"] = "Breaking News"

        elif LastNews.objects.filter(title=news_title).exists():
            news = get_object_or_404(LastNews, title=news_title)
            context["news"] = news
            context["category"] = "Last News"

        # elif Article.objects.get(category=Article.category).exists():
        #     news = get_object_or_404(Article, title=news_title)
        #     context["news"] = news
        #     context["category"] = "Article"

        return context
    
class CategoryNewsDetailView(TemplateView):
    template_name = 'category_news_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        news_slug = self.kwargs.get('news_slug')
        category = get_object_or_404(Category, slug=category_slug)
        article = get_object_or_404(Article, slug=news_slug, category=category)
        
        context['category'] = category
        context['article'] = article
        
        # Add more details about the article
        context['title'] = article.title
        context['author'] = article.author
        context['published_at'] = article.published_at
        context['content'] = article.content
        context['featured_image'] = article.featured_image
        # You might want to add related articles
        related_articles = Article.objects.filter(category=category).exclude(slug=news_slug)[:5]
        context['related_articles'] = related_articles
        comments = Comment.objects.filter(article=article, is_approved=True)
        context['comments'] = comments

        return context

    def get(self, request, *args, **kwargs):
        category_slug = kwargs.get('category_slug')
        news_slug = kwargs.get('news_slug', None)
        if not news_slug:
            return redirect('category_news', category_slug=category_slug)
        return super().get(request, *args, **kwargs)

class CommentView(View):
    def post(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = get_object_or_404(Article, article_id=article_id)
        number = request.POST.get('number')
        comment = request.POST.get('comment')
        Comment.objects.create(article=article, number=number, comment=comment)
        return redirect('category_news_detail', category_slug=article.category.slug, news_slug=article.slug)
    
    
class SubscribeView(TemplateView):
    template_name = 'subscribe.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email') 
        if email:
            if not Subscriber.objects.filter(email=email).exists():
                Subscriber.objects.create(email=email) 
                return redirect('home')
            else:
                return HttpResponse('This email is already subscribed!')
        else:
            return HttpResponse('Please enter a valid email address.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
class CategoryNewsView(TemplateView):
    template_name = 'category_news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = self.kwargs.get('category_name')
        category = get_object_or_404(Category, name=category_name)
        articles = Article.objects.filter(category=category)
        main_article = Article.objects.order_by('-published_at')[:1]
        context['category'] = category
        context['articles'] = articles
        return context

class LivestreamView(TemplateView):
    template_name = "livestream.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        return context

class DonationView(TemplateView):
    template_name = 'donation.html'
    
    def post(self, request, *args, **kwargs):
        # Process form data if needed, though UPI is handled in the frontend
        return self.get(request, *args, **kwargs)
        

