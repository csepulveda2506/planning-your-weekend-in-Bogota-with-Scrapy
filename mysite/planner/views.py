from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Sites


# Create your views here.

class Site:

    def __init__(self, location, title, start_date, description,
                 price, link, end_date=None):
        self.location = location
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.price = price
        self.link = link


class SitesView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_set = Sites.objects.all()
        sites = [Site(location=site.location, title=site.title,
                      start_date=site.startdate,
                      description=site.description, price=site.price,
                      link=site.link) for site in query_set]
        context['sites'] = sites
        return context
