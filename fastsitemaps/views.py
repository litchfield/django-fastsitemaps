from django.conf import settings
from django.core import urlresolvers
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # < Django 1.7
    from django.contrib.sites.models import get_current_site

from fastsitemaps.generator import sitemap_generator
from fastsitemaps.sitemaps import RequestSitemap


SITE_ATTR = getattr(settings, 'FASTSITEMAPS_SITE_ATTR', 'site')


def index(request, sitemaps, template_name='sitemap_index.xml', 
          mimetype='application/xml'):
    current_site = getattr(request, SITE_ATTR, get_current_site(request))
    sites = []
    protocol = 'https' if request.is_secure() else 'http'
    for section, site in sitemaps.items():
        site.request = request
        if callable(site):
            if issubclass(site, RequestSitemap):
                pages = site(request=request).paginator.num_pages
            else:
                pages = site().paginator.num_pages
        else:
            pages = site.paginator.num_pages
        sitemap_url = urlresolvers.reverse('fastsitemaps.views.sitemap', 
                                           kwargs={'section': section})
        sites.append('%s://%s%s' % (protocol, current_site.domain, sitemap_url))
        if pages > 1:
            for page in range(2, pages+1):
                sites.append('%s://%s%s?p=%s' % (protocol, current_site.domain, sitemap_url, page))
    return TemplateResponse(request, template_name, {'sitemaps': sites}, 
                            content_type=mimetype)


def sitemap(request, sitemaps, section=None):
    maps, urls = [], []
    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps.append(sitemaps[section])
    else:
        maps = sitemaps.values()
    page = request.GET.get("p", 1)
    current_site = getattr(request, SITE_ATTR, get_current_site(request))
    return HttpResponse(sitemap_generator(request, maps, page, current_site), 
                        content_type='application/xml')
    
