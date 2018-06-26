from django.views.generic import FormView
try:
    from django.urls import reverse
except IndexError:
    from django.core.urlresolvers import reverse

from .forms import BasicForm


class BasicFormView(FormView):
    template_name = 'form.html'
    form_class = BasicForm

    def get_success_url(self):
        return reverse('form') + '?success=1'
