from django.contrib.sitemaps import Sitemap

class RequestSitemap(Sitemap):
    def __init__(self, request=None):
        self.request = request
        
    def __get(self, name, obj, default=None):
        try:
            attr = getattr(self, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)
        return attr

    def get_urls(self, page=1, site=None, protocol=None):
        "Returns a generator instead of a list, also prevents http: doubling up"
        if site is None:
            if Site._meta.installed:
                try:
                    site = Site.objects.get_current()
                except Site.DoesNotExist:
                    pass
            if site is None:
                raise ImproperlyConfigured("In order to use Sitemaps you must either use the sites framework or pass in a Site or RequestSite object in your view code.")
        for item in self.paginator.page(page).object_list:
            loc = self.__get('location', item)
            if not loc.startswith('http'):
                loc = "http://%s%s" % (site.domain, loc)
            priority = self.__get('priority', item, None)
            url_info = {
                'item':       item,
                'location':   loc,
                'lastmod':    self.__get('lastmod', item, None),
                'changefreq': self.__get('changefreq', item, None),
                'priority':   str(priority is not None and priority or ''),
            }
            yield url_info
