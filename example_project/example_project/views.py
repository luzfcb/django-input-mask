from django.views.generic import FormView

from .forms import BasicForm

try:
    from django.urls import reverse
except IndexError:
    from django.core.urlresolvers import reverse



class BasicFormView(FormView):
    template_name = 'form.html'
    form_class = BasicForm

    def get_success_url(self):
        return reverse('form') + '?success=1'
