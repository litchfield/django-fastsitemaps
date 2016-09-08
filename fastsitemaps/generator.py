from six import StringIO
from django.core.paginator import InvalidPage
from django.http import Http404
from django.utils.xmlutils import SimplerXMLGenerator
from django.conf import settings
from fastsitemaps.sitemaps import RequestSitemap

def sitemap_generator(request, maps, page, current_site):
    output = StringIO()
    protocol = request.is_secure() and 'https' or 'http'
    xml = SimplerXMLGenerator(output, settings.DEFAULT_CHARSET)
    xml.startDocument()
    xml.startElement('urlset', {'xmlns':'http://www.sitemaps.org/schemas/sitemap/0.9'})
    yield output.getvalue()
    pos = output.tell()
    for site in maps:
        if callable(site):
            if issubclass(site, RequestSitemap):
                site = site(request=request)
            else:
                site = site()
        elif hasattr(site, 'request'):
            site.request = request

        try:
            urls = site.get_urls(page=page, site=current_site, protocol=protocol)
        except InvalidPage:
            raise Http404('Page not found')

        for url in urls:
            xml.startElement('url', {})
            xml.addQuickElement('loc', url['location'])
            try:
                if url['lastmod']:
                    xml.addQuickElement('lastmod', url['lastmod'].strftime('%Y-%m-%d'))
            except (KeyError, AttributeError):
                pass
            try:
                if url['changefreq']:
                    xml.addQuickElement('changefreq', url['changefreq'])
            except KeyError:
                pass
            try:
                if url['priority']:
                    xml.addQuickElement('priority', url['priority'])
            except KeyError:
                pass
            xml.endElement('url')
            output.seek(pos)
            yield output.read()
            pos = output.tell()
    xml.endElement('urlset')
    xml.endDocument()
    output.seek(pos)
    last = output.read()
    output.close()
    yield last
