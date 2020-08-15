"""
Originaly code was taken from: http://djangosnippets.org/snippets/290/
But I was made some improvements like:
- print URL from what queries was
- don't show queries from static URLs (MEDIA_URL and STATIC_URL, also for /favicon.ico).
- If DEBUG is False tell to django to not use this middleware
- Remove guessing of terminal width (This breaks the rendered SQL)
"""
try:
    import cProfile as profile
except ImportError:
    import profile

import pstats

from clint.textui import colored, columns, indent, puts
from cStringIO import StringIO
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.db import connection


INDENTATION = 2


class ProfilerMiddleware(object):
    """
    Originaly code was taken from:
    https://github.com/omarish/django-cprofile-middleware/blob/master/django_cprofile_middleware/middleware.py

    Simple profile middleware to profile django views. To run it, add ?prof to
    the URL like this:

        http://localhost:8000/view/?prof

    Optionally pass the following to modify the output:

    ?sort => Sort the output by a given metric. Default is time.
        See http://docs.python.org/2/library/profile.html#pstats.Stats.sort_stats
        for all sort options.

    ?count => The number of rows to display. Default is 100.

    This is adapted from an example found here:
    http://www.slideshare.net/zeeg/django-con-high-performance-django-presentation.
    """
    def can(self, request):
        return settings.DEBUG and 'prof' in request.GET and \
            request.user is not None and request.user.is_staff

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if self.can(request):
            self.profiler = profile.Profile()
            args = (request,) + callback_args
            try:
                value = self.profiler.runcall(callback, *args, **callback_kwargs)
                return value
            except:
                # we want the process_exception middleware to fire
                # https://code.djangoproject.com/ticket/12250
                return

    def process_response(self, request, response):
        if self.can(request):
            self.profiler.create_stats()
            io = StringIO()
            stats = pstats.Stats(self.profiler, stream=io)
            stats.strip_dirs().sort_stats(request.GET.get('sort', 'time'))
            stats.print_stats(int(request.GET.get('count', 100)))
            value = io.getvalue()
            with indent(INDENTATION):
                puts(colored.magenta('[Profile Information for] ') + colored.blue(request.path_info))
                puts()
                puts(value)
        return response


class SQLPrintingMiddleware(object):
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed. This is only useful for debugging.
    """
    def __init__(self):
        if not settings.DEBUG:
            raise MiddlewareNotUsed

    def process_response(self, request, response):
        if (len(connection.queries) == 0 or
                request.path_info.startswith('/favicon.ico') or
                request.path_info.startswith(settings.STATIC_URL) or
                request.path_info.startswith(settings.MEDIA_URL)):
            return response

        with indent(INDENTATION):
            puts(colored.magenta('[SQL Queries for] ') + colored.blue(request.path_info))
            puts()
            total_time = 0.0
            for query in connection.queries:
                nice_time = '[{0}]'.format(query['time'])
                nice_sql = query['sql'].replace('"', '').replace(',', ', ')
                total_time = total_time + float(query['time'])
                puts(
                    columns(
                        [colored.red(nice_time), 10],
                        [colored.white(nice_sql), 120],
                    )
                )
                puts()
            puts(colored.green("[TOTAL TIME: %s seconds (%s queries)]" % (str(total_time), str(len(connection.queries)))))
        return response
