from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import ArticleForm, CommentForm
from .mixins import AuthorAndLoginRequiredMixin
from .models import Article, Category


class ArticleListView(generic.ListView):
    """
    Обработчик вывода списка опубликованных статей.
    """
    template_name = 'blog/article/article_list.html'

    paginate_by = 4

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug', None)
        category = None
        queryset = Article.objects.filter(status='STATUS_PUBLISHED')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset


class ArticleOwnerListView(ArticleListView, AuthorAndLoginRequiredMixin):
    """
    Обработчик вывода списка всех статей принадлежащих юзеру.
    """
    queryset = Article.objects.all()


class ArticleDetailView(generic.DetailView):
    """
    Обработчик вывода информации конкретной статьи.
    """
    template_name = 'blog/article/article_detail.html'
    queryset = Article.objects.all()
    form = CommentForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, pk):
        """
        Метод выводит форму для комментария.
        """
        form = CommentForm(request.POST)
        article = Article.objects.get(id=pk)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.article = article
            form.save()
            return redirect(article.get_absolute_url())


class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Обработчик вывода формы для Создания статьи.
    Для всех зарегистрированных пользователей.
    """
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article/article_create_form.html'


class ArticleUpdateView(AuthorAndLoginRequiredMixin, generic.UpdateView):
    """
    Обработчик вывода формы для редактирования конкретной статьи.
    Для автора статьи.
    """
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article/article_update_form.html'


class ArticleDeleteView(AuthorAndLoginRequiredMixin, generic.DeleteView):
    """
    Обработчик удаления конкретной статьи автором статьи.
    """
    model = Article
    template_name = 'blog/article/article_confirm_delete.html'
    success_url = reverse_lazy('blog:article_list')


class SearchView(ArticleListView):
    """
    Обработчик поиска по названию и описанию статьи.
    Наследуемся от ArticleListView с переназначением метода get.
    """
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        context = {
            'article_list': queryset
        }
        return render(request, 'blog/article/article_list.html', context)
