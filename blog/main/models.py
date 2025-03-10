from autoslug import AutoSlugField
from django.db import models
from slugify import slugify
from django.utils import timezone

class user(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from = "name", unique=True, null=False, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class blog(models.Model):
    STATUS = [
        ('0',"DRAFT"),
        ('1','PUBLISHED')
    ]
    author = models.ForeignKey(user,related_name='author',on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images")
    category = models.ForeignKey(category,related_name='category',on_delete=models.CASCADE)
    blog_slug = AutoSlugField(populate_from="title",unique=True,null=False,default=None)
    status = models.CharField(choices=STATUS,max_length=100,default=0)
    updated_at = models.DateTimeField(auto_now=True)
    # main_post = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title} ({self.category})"

class comments(models.Model):
    post = models.ForeignKey(blog,related_name='comments',on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(user,related_name='cuser',on_delete=models.CASCADE)
    date_time = models.DateField(default=timezone.now)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name
