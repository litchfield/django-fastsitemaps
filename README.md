Drop-in replacement for django.contrib.sitemaps.

Extras --

- Streaming sitemaps response via sax (provided your middlewares don't interfere)
  Big sitemaps load much faster and use way less memory (O^1 not O^n).
- Allows access to "request" from sitemap object (using RequestSitemap).
- Optionally determins current_site from request object.
  (See settings.FASTSITEMAPS_SITE_ATTR attribute- default 'site', ie request.site)
  This can be useful if you are running multiple "sites" in one app instance.

