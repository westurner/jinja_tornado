# coding: utf-8
from jinja2 import Environment, FileSystemLoader, Markup
import json
import datetime
from tornado.escape import ( squeeze, linkify, url_escape, xhtml_escape )

class JinjaApp(object):
    def __init__(self, application, jinja_options=None):
        self.application = application
        self.jinja_options = jinja_options
        self.init_app(application, jinja_options)

    @classmethod
    def _make_decorators(cls, jinja_environ):
        def template_filter(name=None):
            def decorator(f):
                jinja_environ.filters[name or f.__name__] = f
            return decorator

        def template_test(name=None):
            def decorator(f):
                jinja_environ.tests[name or f.__name__] = f
            return decorator

        def template_global(name=None):
            def decorator(f):
                jinja_environ.globals[name or f.__name__] = f
            return decorator

        jinja_environ.template_filter = template_filter
        jinja_environ.template_test = template_test
        jinja_environ.template_global = template_global

    @classmethod
    def init_app(cls, application, jinja_options=None):

        app_settings = application.settings

        # although flask uses different loader that can handle blueprints, tornado has no concept of blueprints we'll resort to simple FileSystemLoader.
        _loader = FileSystemLoader(
            app_settings.get('template_path', 'templates')
        )

        # those default values are copied from defaults of jinja2 and(or) flask.
        _jinja_config = dict(
              extensions  = ['jinja2.ext.autoescape', 'jinja2.ext.with_']
            , auto_reload = app_settings.get('autoreload', False)
            , loader      = _loader
            , cache_size  = 50 if app_settings.get('compiled_template_cache', True) else 0
            , autoescape  = True if app_settings.get('autoescape', 'xhtml_escape') == "xhtml_escape" else False
            )

        _jinja_config.update(**(jinja_options or {}))
        environment = Environment(**_jinja_config)

        application.jinja_environment = environment
        app_settings['jinja_environment'] = environment
        cls._make_decorators(environment)
        environment.filters.update(
              tojson       = tojson_filter
            , xhtml_escape = xhtml_escape
            , url_escape   = url_escape
            , squeeze      = squeeze
            , linkify      = linkify
        )

        return environment

def dumps(obj, **kwargs):
    # https://github.com/mitsuhiko/flask/blob/master/flask/json.py
    rv = json.dumps(obj, **kwargs) \
        .replace('<', '\\u003c') \
        .replace('>', '\\u003e') \
        .replace('&', '\\u0026') \
        .replace("'", '\\u0027')

    return rv

def tojson_filter(obj, **kwargs):
    # https://github.com/mitsuhiko/flask/blob/master/flask/json.py
    return Markup(dumps(obj, **kwargs))


class JinjaTemplateMixin(object):
    """usage:
        class JinjaPoweredHandler(JinjaTemplateMixin, tornado.web.RequestHandler):
            pass
    """

    def initialize(self, *args, **kwargs):
        super(JinjaTemplateMixin, self).initialize(*args, **kwargs)

        # jinja environment is shared among an application
        if not 'jinja_environment' in self.application.settings:
            raise RuntimeError("Needs jinja2 Environment. Initialize with JinjaApp.init_app first")

        else:
            self._jinja_env = self.application.settings['jinja_environment']

    @property
    def session(self):
        """ implementation of a session that matches flask's session.
        fixme: don't force secure_cookie based sessions to everyone."""
        if not hasattr(self, '_session'):
            cookie = self.get_secure_cookie('session')
            if cookie:
                self._session = json.loads(cookie)
            else:
                self._session = {}

        return self._session

    def _render(self, template, **kwargs):
        """ todo: support multiple template preprocessors """

        def _ctx_processor():
            rv = dict(
              request        = self.request
            , session        = self.session
            , path_args      = self.path_args
            , path_kwargs    = self.path_kwargs
            , settings       = self.application.settings
            , reverse_url    = self.application.reverse_url
            , static_url     = self.static_url
            , xsrf_form_html = self.xsrf_form_html
            , datetime       = datetime
            , locale         = self.locale
            , _              = self.locale.translate
            , handler        = self
            , current_user   = self.current_user
            )
            return rv

        ctx = _ctx_processor()
        ctx.update(kwargs)
        return template.render(ctx)

    def render(self, template_name, **kwargs):
        """ renders a template file. """
        template = self._jinja_env.get_template(template_name)
        html = self._render(template, **kwargs)
        self.finish(html)

    def render_string(self, source, **kwargs):
        """ renders a template source string. """
        template = self._jinja_env.from_string(source)
        return self._render(template, **kwargs)

    def finish(self, chunk=None):
        """ because of 'session', send the cookies to clients before finishing it """
        self.set_secure_cookie('session', json.dumps(self.session))
        super(JinjaTemplateMixin, self).finish(chunk)
