from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
def index(request):
    return render_to_response("templates/index.html", locals(),
    context_instance=RequestContext(request))
