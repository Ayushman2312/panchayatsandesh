from typing import Any
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.hashers import check_password

import logging

# Configure logger
logger = logging.getLogger(__name__)

def Login(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            password_check = check_password(password, user_obj.password)
            if password_check:
                request.session['user_id'] = str(user_obj.user_id)
                return redirect('messages')
            else:
                messages.error(request, 'Wrong password')
                return redirect('panchayatuser')
        except User.DoesNotExist:
            messages.info(request, 'Email does not exist')
            return redirect('panchayatuser')
    return render(request, 'login.html')

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
        # Get all articles ordered by creation date
        # Get all published articles
        all_news = Article.objects.filter(status='Published').order_by('-created_at')
        
        # Add all news to context without filtering
        context["all_news"] = all_news
        all_categories = Category.objects.all()
        news_by_category = {}
        for category in all_categories:
            news_by_category[category] = Article.objects.filter(category=category).order_by('-created_at')
        context["news_by_category"] = news_by_category
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
        comments = Comment.objects.filter(article=article)
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
        main_article = Article.objects.order_by('-created_at')[:1]
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
        

class CommunicationView(TemplateView):
    template_name = 'communicate.html'

    def get_context_data(self, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("Entering CommunicationView.get_context_data")
        
        context = super().get_context_data(**kwargs)
        
        logger.debug("Returning context from CommunicationView.get_context_data")
        return context
    
    def post(self, request, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("Entering CommunicationView.post")
        
        whatsapp_number = request.POST.get('whatsapp_number')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        logger.debug(f"Received form data - WhatsApp: {whatsapp_number}, Email: {email}, Message length: {len(message) if message else 0}")
        
        if whatsapp_number and email and message:
            try:
                # Create a new communication record
                logger.debug("Creating new communication record")
                comm = communication.objects.create(
                    whatsapp_number=whatsapp_number,
                    email=email,
                    message=message
                )
                logger.debug(f"Communication record created with ID: {comm.id}")
                
                messages.success(request, 'Your message has been sent successfully!')
                logger.debug("Redirecting to home page after successful submission")
                return redirect('home')
            except Exception as e:
                logger.error(f"Error creating communication record: {str(e)}")
                messages.error(request, 'An error occurred while sending your message.')
                return self.get(request, *args, **kwargs)
        else:
            logger.warning("Form submission missing required fields")
            messages.error(request, 'Please fill all required fields.')
            return self.get(request, *args, **kwargs)

class MessagesView(TemplateView):
    template_name = 'messages.html'
    
    def get_context_data(self, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("Entering MessagesView.get_context_data")
        
        context = super().get_context_data(**kwargs)
        
        # Get all communications
        logger.debug("Fetching all communications ordered by creation date")
        communications_list = communication.objects.all().order_by('-created_at')
        logger.debug(f"Retrieved {communications_list.count()} communication records")
        
        context['communications'] = communications_list
        # context['message'] =
        
        logger.debug("Returning context from MessagesView.get_context_data")
        return context
    
    def post(self, request, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("Entering MessagesView.post")
        
        communication_id = request.POST.get('communication_id')
        response_message = request.POST.get('response')
        
        logger.debug(f"Processing response for communication ID: {communication_id}")
        logger.debug(f"Response message length: {len(response_message) if response_message else 0}")
        
        if communication_id and response_message:
            try:
                # Get the communication object
                logger.debug(f"Retrieving communication with ID: {communication_id}")
                comm = communication.objects.get(id=communication_id)
                logger.debug(f"Found communication from: {comm.email}")
                
                # Update the communication with response and mark as viewed
                logger.debug("Updating communication with response and marking as viewed")
                comm.response = response_message
                comm.viewed = True
                comm.save()
                logger.debug("Communication record updated successfully")
                
                # Send email to the user
                from django.core.mail import send_mail
                from django.conf import settings
                
                subject = 'Response to your message - Panchayat Sandesh'
                email_body = f"""
                Dear User,
                
                Thank you for contacting Panchayat Sandesh. Here is our response to your inquiry:
                
                {response_message}
                
                If you have any further questions, please feel free to contact us again.
                
                Best regards,
                Panchayat Sandesh Team
                """
                
                logger.debug(f"Sending email response to: {comm.email}")
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [comm.email],
                    fail_silently=False,
                )
                logger.debug("Email sent successfully")
                
                messages.success(request, 'Response sent successfully!')
            except communication.DoesNotExist:
                logger.error(f"Communication with ID {communication_id} not found")
                messages.error(request, 'Communication not found.')
            except Exception as e:
                logger.error(f"Error sending response: {str(e)}")
                messages.error(request, f'Error sending response: {str(e)}')
        else:
            logger.warning("Missing communication ID or response message")
            messages.error(request, 'Please provide a response message.')
            
        logger.debug("Redirecting to messages page")
        return redirect('messages')
