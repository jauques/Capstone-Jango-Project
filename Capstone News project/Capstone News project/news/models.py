"""
Database models for the News Application.

This module defines the main data structures used by the project:
CustomUser, Publisher, Article and Newsletter. These models describe
how users, publishers, articles and newsletters are stored in the
MariaDB database through Django's ORM.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model for the News Application.

    This model extends Django's built-in AbstractUser so that each
    user can be assigned a specific application role: Reader,
    Journalist, or Editor.

    Readers can subscribe to publishers and journalists. These
    subscription relationships are used by the subscribed articles
    API endpoint to return content relevant to the logged-in reader.
    """

    ROLE_CHOICES = [
        ('Reader', 'Reader'),
        ('Journalist', 'Journalist'),
        ('Editor', 'Editor'),
    ]

    # Stores the role used for role-based access control.
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    # Allows readers to subscribe to one or more publishers.
    subscriptions_publishers = models.ManyToManyField(
        'Publisher',
        blank=True,
        related_name='subscribers'
    )

    # Allows readers to subscribe to one or more journalist users.
    subscriptions_journalists = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='journalist_subscribers'
    )

    def __str__(self):
        """
        Return the username as the readable display value.

        This makes user records easier to identify in Django Admin
        and in relationship dropdown fields.
        """
        return self.username


class Publisher(models.Model):
    """
    Represents a news publisher.

    A publisher can have many articles linked to it. Readers can also
    subscribe to publishers so that they can retrieve articles from
    selected publishers using the subscribed articles API endpoint.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        """
        Return the publisher name for readable display.
        """
        return self.name


class Article(models.Model):
    """
    Represents a news article created by a journalist.

    Each article has an author, optional publisher, creation date,
    and approval status. The approved field controls whether the
    article is visible through the public article API responses.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()

    # Links each article to the user who created it.
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    # Links the article to a publisher. SET_NULL keeps the article
    # available even if the publisher record is removed.
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Editors can use this field to mark articles as approved.
    approved = models.BooleanField(default=False)

    def __str__(self):
        """
        Return the article title for readable display.
        """
        return self.title


class Newsletter(models.Model):
    """
    Represents a newsletter created by a journalist.

    A newsletter can contain multiple articles through a ManyToMany
    relationship. This allows one newsletter to group several articles
    together for readers.
    """

    title = models.CharField(max_length=200)

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Links each newsletter to the user who created it.
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='newsletters'
    )

    # Allows a newsletter to contain multiple articles.
    articles = models.ManyToManyField(
        Article,
        blank=True
    )

    def __str__(self):
        """
        Return the newsletter title for readable display.
        """
        return self.title
