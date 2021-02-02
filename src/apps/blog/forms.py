from django import forms

from .models import Article, Comment


class SearchForm(forms.Form):
    """
    Форма для поиска по статьям.
    """
    query = forms.CharField()


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'slug', 'category', 'poster', 'description', 'content',
                  'status', 'allow_comments', 'previous_article', 'next_article', 'tags')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )
