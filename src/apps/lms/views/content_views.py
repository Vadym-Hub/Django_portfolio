from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.apps import apps
from django.views import generic
from django.views.generic.base import TemplateResponseMixin


from ..models import Module, Content


class ModuleContentListView(TemplateResponseMixin, generic.View):
    """
    Обработчик получает из базы данных модуль по переданному ID
    и генерирует для него страницу подробностей.
    """
    template_name = 'lms/manage/module/module_content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})


class ContentCreateUpdateView(TemplateResponseMixin, generic.View):
    """
    Обработчик, который позволят создать, изменить или удалить содержимое модуля.
    """
    module = None
    model = None
    obj = None
    template_name = 'lms/manage/module/content/content_form.html'

    def get_model(self, model_name):
        """Возвращает класс модели по переданному имени."""
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='lms', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """Создает форму в зависимости от типа содержимого."""
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """Получает данные из запроса и создает соответствующие объекты модуля."""
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        """Формирует модельные формы для объектов Text, Video, Image или File."""
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        """
        Если форма заполнена корректно, создает новый объект, указав
        текущего пользователя, request.user, владельцем.
        """
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # Создаем новый объект.
                Content.objects.create(module=self.module, item=obj)
            return redirect('lms:module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(generic.View):
    """
    Обработчик удаления контента модуля.
    """
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('lms:module_content_list', module.id)
