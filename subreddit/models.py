from django.db import models
from reddit_clone.settings import AUTH_USER_MODEL


class SubReddit(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="subreddits/", null=True, blank=True)
    subscribers = models.ManyToManyField(
        AUTH_USER_MODEL, related_name="subreddits", through="Subscription"
    )
    moderators = models.ManyToManyField(
        AUTH_USER_MODEL, related_name="moderated_subreddits", through="Moderator"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Subreddit"
        verbose_name_plural = "Subreddits"


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, null=True, blank=True)
    subreddit = models.ForeignKey(
        SubReddit, on_delete=models.CASCADE, related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Comment(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Rules(models.Model):
    subreddit = models.ForeignKey(
        SubReddit, on_delete=models.CASCADE, related_name="rules"
    )
    rule = models.TextField()
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.rule

    class Meta:
        ordering = ("order",)
        verbose_name = "Rule"
        verbose_name_plural = "Rules"


class PostVote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.post}"

    class Meta:
        verbose_name = "Post Vote"
        verbose_name_plural = "Post Votes"
        unique_together = ("user", "post")


class CommentVote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.comment}"

    class Meta:
        verbose_name = "Comment Vote"
        verbose_name_plural = "Comment Votes"
        unique_together = ("user", "comment")


class Subscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    subreddit = models.ForeignKey(SubReddit, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "subreddit")


class Moderator(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    subreddit = models.ForeignKey(SubReddit, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "subreddit")
