import django
from django import forms


class MultiSelectWidget(forms.MultiWidget):
    template_name = 'gadjo/widgets/multiselectwidget.html'

    class Media:
        js = ('js/gadjo.multiselectwidget.js',)
        css = {'all': ('css/gadjo.multiselectwidget.css',)}

    def __init__(self, attrs=None):
        self.attrs = attrs
        widgets = [forms.Select(attrs=attrs)]
        super().__init__(widgets, attrs)

    def get_context(self, name, value, attrs):
        if not isinstance(value, list):
            value = [value]

        self.widgets = []
        for _ in range(max(len(value), 1)):
            self.widgets.append(forms.Select(attrs=self.attrs, choices=self.choices))

        # all subwidgets must have the same name
        if django.VERSION >= (3, 1):
            self.widgets_names = [''] * len(self.widgets)
            return super().get_context(name, value, attrs)
        else:
            context = super().get_context(name, value, attrs)
            subwidgets = context['widget']['subwidgets']
            for widget in subwidgets:
                widget['name'] = widget['name'].rsplit('_', 1)[0]
            return context

    def decompress(self, value):
        return value or []

    def value_from_datadict(self, data, files, name):
        values = [x for x in data.getlist(name) if x]

        # remove duplicates while keeping order
        return list(dict.fromkeys(values))

    def id_for_label(self, id_):
        return id_
