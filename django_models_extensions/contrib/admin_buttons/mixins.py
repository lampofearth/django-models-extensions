from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.functional import cached_property


def admin_button_handler(name=None, **handler_kwargs):
    def decorator(func):
        func.bind_to_handler = True
        func.kwargs = handler_kwargs
        func.handler_name = name if name is not None else func.__name__

        return func

    return decorator


class AdminButtonMixin(admin.ModelAdmin):
    change_list_buttons = []
    change_form_buttons = []

    buttons_url_prefix = 'button_handler'

    change_list_template = "admin/admin_buttons/admin_buttons_change_list.html"
    change_form_template = "admin/admin_buttons/admin_buttons_change_form.html"

    handlers = dict()

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        for handler in dir(self):
            _obj = getattr(self, handler)
            if getattr(_obj, 'bind_to_handler', False) == True:
                self.handlers.update({_obj.handler_name: _obj})

    @cached_property
    def app_name(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        return '{}_{}'.format(*info)

    @cached_property
    def app_name_changelist(self):
        return f'{self.app_name}_changelist'

    @cached_property
    def app_name_changeform(self):
        return f'{self.app_name}_change'

    def get_urls(self):

        _urls = []

        def _clear_data(data):
            return data.replace('/', '_').replace(' ', '_').lower()

        def _generate_url():
            url = url_head + url_tail

            name_tail = _clear_data(url_tail)
            name = '{}_{}'.format(self.app_name, name_tail)

            button.update({'url': name_tail})

            handler = self.handlers.get(button['handler'], None)
            _urls.append(path(url, handler, name=name))

        for button in self.change_list_buttons:
            _name = _clear_data(button['name'])
            button.setdefault('handler', _name)

            url_head = ''
            url_tail = f"{self.buttons_url_prefix}/{_name}"

            _generate_url()

        for button in self.change_form_buttons:
            _name = _clear_data(button['name'])
            button.setdefault('handler', _name)

            url_head = '<path:object_id>/'
            url_tail = f'{self.buttons_url_prefix}/{_name}'

            _generate_url()

        urls = super().get_urls()
        return _urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = {'change_list_buttons': self.change_list_buttons}

        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='',
                        extra_context=None):
        extra_context = {'change_form_buttons': self.change_form_buttons}

        return super().changeform_view(request, object_id, form_url,
                                       extra_context)

    def redirect_to_change_list(self, request):
        """
        :param request:
        :return:
        """
        opts = self.model._meta
        preserved_filters = self.get_preserved_filters(request)

        redirect_url = add_preserved_filters(
            {'preserved_filters': preserved_filters, 'opts': opts},
            reverse('admin:' + self.app_name_changelist))
        return HttpResponseRedirect(redirect_url)
