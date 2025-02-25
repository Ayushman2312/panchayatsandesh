from django.db import models
import uuid
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.user_id + " " + self.username
    
STATUS = (
    ('Published', 'Published'),
    ('Archive', 'Archive'),
    ('Not Published', 'Not Published'),
)

class Category(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(unique = True)
    image = models.ImageField(upload_to="images/category_images", default="images/panchayat_sandesh_logo.png")

    def __str__(self):
        return self.name
    
class Article(models.Model):
    article_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length = 100)
    slug = models.SlugField(unique = True)
    description = models.TextField(default = 100)
    author = models.CharField(max_length = 100, default = "Anurag Tiwari")
    content = models.TextField()
    published_at = models.DateTimeField()
    featured_image = models.ImageField(upload_to='media/images')
    status = models.CharField(max_length = 100, choices = STATUS)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    blogpost_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length = 100)
    slug = models.SlugField(unique = True)
    author = models.CharField(max_length = 100, default = "Anurag Tiwari")
    content = models.TextField()
    published_at = models.DateTimeField()
    featured_image = models.ImageField(upload_to='media/images')
    status = models.CharField(max_length = 100, choices = STATUS)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Magazine(models.Model):
    magazine_id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)
    magazine_title = models.CharField(max_length = 100, default= "none")
    issue_number = models.IntegerField()
    description = models.TextField()
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to = 'images/magazine/')
    pdf_file = models.FilePathField(path='media/pdfs/', match=None, max_length=100)

    def __str__(self):
        return self.magazine_title

class HotNewsImage(models.Model):
    image = models.ImageField(upload_to="images/hot-news/",default="images/panchayat_sandesh_logo.png")
    image_name = models.CharField(max_length=100)

class HotNews(models.Model):
    news_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    content = models.TextField()
    author = models.CharField(max_length = 100, default = 'Anurag Tiwari')
    created_at = models.DateTimeField(null = True, blank=True)
    image = models.ForeignKey(HotNewsImage, on_delete = models.CASCADE)

class TrendingNewsImage(models.Model):
    image = models.ImageField(upload_to="images/trending-news/", default="images/panchayat_sandesh_logo.png")
    image_title = models.CharField(max_length=100)

    def __str__(self):
        return self.image_title

class TrendingNews(models.Model):
    news_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    content = models.TextField()
    images = models.ForeignKey(TrendingNewsImage, on_delete = models.CASCADE)
    author = models.CharField(max_length = 100, default = 'Anurag Tiwari')
    created_at = models.DateTimeField(null = True, blank=True, default = timezone.now)

    def __str__(self):
        return self.title
    
class BreakingNewsImage(models.Model):
    image = models.ImageField(upload_to="images/breaking-news/", default="images/panchayat_sandesh_logo.png")
    image_title = models.CharField(max_length=100)

    def __str__(self):
        return self.image_title

class BreakingNews(models.Model):
    news_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    content = models.TextField()
    images = models.ForeignKey(BreakingNewsImage, on_delete = models.CASCADE)
    author = models.CharField(max_length = 100, default = 'Anurag Tiwari')
    created_at = models.DateTimeField(null = True, blank=True)

    def __str__(self):
        return self.title
    

class LastNewsImage(models.Model):
    image = models.ImageField(upload_to="images/last-news/", default="images/panchayat_sandesh_logo.png")
    image_title = models.CharField(max_length=100)

    def __str__(self):
        return self.image_title

class LastNews(models.Model):
    news_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    content = models.TextField()
    images = models.ForeignKey(LastNewsImage, on_delete = models.CASCADE)
    author = models.CharField(max_length = 100, default = 'Anurag Tiwari')
    created_at = models.DateTimeField(null = True, blank=True)

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class GalleryImages(models.Model):
    image = models.ImageField(upload_to="images/gallery_images")
    name = models.CharField(max_length = 100, default = "gallery_image")

    def __str__(self):
        return self.name

    
class Donations(models.Model):
    name = models.CharField(max_length = 100)
    mobile_number = models.PositiveBigIntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name
    
class UpcomingEvents(models.Model):
    event_name = models.CharField(max_length = 100)
    event_description = models.TextField()
    no_of_registers = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.event_name
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})
    
class EventRegistration(models.Model):
    event = models.ForeignKey(UpcomingEvents, on_delete=models.CASCADE, null=True, related_name='registrations')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    # Add other fields as needed (e.g., phone number, company, etc.)

    def __str__(self):
        return f"{self.name} - {self.event.event_name}"
    

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    number = models.CharField(max_length=10, null=True)
    comment = models.TextField(null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.number} - {self.article.title}"
