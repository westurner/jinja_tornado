jinja_tornado
=============

jinja2 support for tornado applications.

## Usage

    from jinja_tornado import JinjaApp, JinjaTemplateMixin

    application = tornado.web.Application( ... )

    environment = JinjaApp.init_app(application) 
    """init_app returns jinja2 environment that is used by application.
    takes a dict as second argument which contains your custom jinja 2
    settings for environment constructor.
    see http://jinja.pocoo.org/docs/api/#jinja2.Environment """



    class JinjaEnabledHandler(JinjaTemplateMixin, tornado.web.RequestHandler):
        """ this Handler supports
            - `self.session` properties (as flask.session) and `session` in template
            - `self.render` method
            - `self.render_string` method """




    # custom filters, tests, globals
    environment = JinjaApp.init_app(application)
    @environment.filter()
    def foo_to_bar(x):
        return x.replace('foo', 'bar')

## Template variables

    request => tornado.web.RequestHandler.request
    session => tornado.web.RequestHandler.get_secure_cookie('session')
    path_args => tornado.web.RequestHandler.path_args
    path_kwargs => tornado.web.RequestHandler.path_kwargs
    settings => tornado.web.RequestHandler.application.settings
    reverse_url => tornado.web.RequestHandler.application.reverse_url
    static_url => tornado.web.RequestHandler.static_url
    xsrf_form_html => tornado.web.RequestHandler.xsrf_form_html


## Todo

- write tests
- no more opinionated `session` implementation
- implement template preprocessors
- UIModules, and various 'tornado' template structures

## License

MIT
