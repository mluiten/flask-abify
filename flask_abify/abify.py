from .utils import _default_storage
from .models import Experiment, Split

from .extension import AbifyExtension

class ABify:
    def __init__(self, app, session=None, storage=None):
        self.storage = storage or _default_storage()

        if session is None:
            app.session['abify'] = dict()
            session = app.session['abify']
        self.session = session

        # Add support for the abify jinja2 extention
        app.jinja_env.add_extension(AbifyExtension)
        app.abify = self

    def start(self, name, *splits):
        """ Starts or resumes a A/B split test """
        experiment = Experiment(self, name, *splits)
        return experiment

    def complete(self, name):
        experiment = Experiment(self, name).load()
