from django.contrib import admin
from subreddit.models import SubReddit, Post, Comment, Rules

# Register your models here.
admin.site.register(SubReddit)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Rules)
