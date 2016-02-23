###Fast, streaming sitemaps for Django

Drop-in replacement for django.contrib.sitemaps that gives you fast, streaming sitemaps that consume minimal memory (O^1 instead of O^n) and minimal server response time on huge data sets.

If you've got sitemaps with millions of urls, this is your friend.

####Usage

1. pip install django-fastsitemaps
2. Update your url patterns to use 'fastsitemaps' instead of 'django.contrib.sitemaps'

####Example

Instead of something like this --

	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemap_dict}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap_dict}),

Try this --

	url(r'^sitemap\.xml$', 'fastsitemaps.views.index', {'sitemaps': sitemap_dict}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'fastsitemaps.views.sitemap', {'sitemaps': sitemap_dict}),

It's not necessary, but you might also choose to add 'fastsitemaps' to your INSTALLED_APPS just to remind and inform yourself and your buddies that you're using it.

####Varying sitemaps by request/site

Another little optional and somewhat unrelated freebie that's included here is fastsitemaps.RequestSitemap, which is the same as Sitemap but gives you access to the request object, via self.request. It can be handy for sitemaps that vary based on site or host name. 

You can also set settings.FASTSITEMAPS_SITE_ATTR to the name of a property on your request object (eg set via middleware) at which it can expect the current site (eg 'site' for request.site). That site's domain will then be used in urls throughout the sitemap.

####Summary

- Streaming sitemaps response via sax (provided your middlewares don't interfere)
  Big sitemaps load much faster and use way less memory (O^1 not O^n).
- Allows access to "request" from sitemap object (using RequestSitemap).
- Optionally determines current_site from request object.
  (See settings.FASTSITEMAPS_SITE_ATTR attribute- default 'site', ie request.site)
  This can be useful if you are running multiple "sites" in one app instance.

####Future

It'd be nice to include a simple on/off setting that causes your sitemaps to be served from disk; and a celery task and management command to trigger the pre-rendering to disk.
