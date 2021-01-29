from django import forms

from .models import Article, Comment


class SearchForm(forms.Form):
    """
    Форма для поиска по статьям.
    """
    query = forms.CharField()


class ArticleForm(forms.ModelForm):
    # content = forms.CharField(
    #     widget=TinyMCEWidget(
    #         attrs={'required': False, 'cols': 30, 'rows': 10}
    #     )
    # )

    class Meta:
        model = Article
        fields = ('title', 'slug', 'category', 'poster', 'description', 'content',
                  'status', 'allow_comments', 'previous_article', 'next_article', 'tags')


class CommentForm(forms.ModelForm):
    # content = forms.CharField(widget=forms.Textarea(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Поле для комментария',
    #     'id': 'usercomment',
    #     'rows': '4'
    # }))

    class Meta:
        model = Comment
        fields = ('content', )
