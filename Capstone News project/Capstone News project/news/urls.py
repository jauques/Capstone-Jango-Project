"""
URL routes for the News Application API.

This module maps API URL paths to the Django REST Framework views
that handle article listing, article details and subscribed content.
"""

from django.urls import path

from .views import (
    ArticleListView,
    ArticleDetailView,
    SubscribedArticlesView,
)


urlpatterns = [
    # Lists approved articles and supports article creation.
    path(
        'articles/',
        ArticleListView.as_view(),
        name='article-list'
    ),

    # Lists approved articles from subscribed publishers or journalists.
    path(
        'articles/subscribed/',
        SubscribedArticlesView.as_view(),
        name='subscribed-articles'
    ),

    # Retrieves, updates or deletes a specific article by primary key.
    path(
        'articles/<int:pk>/',
        ArticleDetailView.as_view(),
        name='article-detail'
    ),
]
