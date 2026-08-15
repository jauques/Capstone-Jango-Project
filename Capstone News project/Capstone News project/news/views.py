"""
API views for the News Application.

This module contains the Django REST Framework views that expose
article data through authenticated API endpoints. It also applies
role-based permission checks for readers, journalists and editors.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Article
from .serializers import ArticleSerializer
from .permissions import IsEditor, IsJournalist


class ArticleListView(generics.ListCreateAPIView):
    """
    List approved articles and allow journalists to create articles.

    GET requests return approved articles only.
    POST requests require the user to be authenticated and to have
    the Journalist role.
    """

    queryset = Article.objects.filter(approved=True)
    serializer_class = ArticleSerializer

    def get_permissions(self):
        """
        Apply permissions based on the HTTP method.
        """

        if self.request.method == "POST":
            return [IsAuthenticated(), IsJournalist()]

        return [IsAuthenticated()]


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single article.

    Authenticated users can retrieve article details.
    Journalists and editors can update and delete articles.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        """
        Apply role-based permissions for article actions.
        """

        if self.request.method == "DELETE":
            if self.request.user.role in ["Editor", "Journalist"]:
                return [IsAuthenticated()]
            return [IsAuthenticated(), IsEditor()]

        if self.request.method in ["PUT", "PATCH"]:
            if self.request.user.role in ["Editor", "Journalist"]:
                return [IsAuthenticated()]
            return [IsAuthenticated(), IsJournalist()]

        return [IsAuthenticated()]


class SubscribedArticlesView(generics.ListAPIView):
    """
    Return approved articles from subscribed publishers or journalists.

    This endpoint is intended for reader users. It checks the logged-in
    user's publisher and journalist subscriptions, then returns approved
    articles that match those subscriptions.
    """

    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Build a queryset of approved articles for the current user.

        The result combines articles from subscribed publishers with
        articles written by subscribed journalists.
        """

        user = self.request.user

        publishers = user.subscriptions_publishers.all()
        journalists = user.subscriptions_journalists.all()

        return (
            Article.objects.filter(
                approved=True,
                publisher__in=publishers
            )
            |
            Article.objects.filter(
                approved=True,
                author__in=journalists
            )
        )