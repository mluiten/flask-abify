from utils import check_uniqueness

class Experiment:
    def __init__(self, abify, name, *splits):
        self.abify = abify
        self.name = name

        if name.startswith('__'):
            raise ValueError('Experiment name cannot start with __')

        if check_uniqueness(splits):
            self.splits = [Split(self, x) for x in splits]
        else:
            raise ValueError("Split names must be unique")

    def load(self):
        """ Load the experiment from the storage """
        instance = self.abify.storage.load_experiment(self.name)
        self.splits = [Split(self, x) for x in instance['splits']]

    def save(self):
        """ Save the experiment to the storage """
        self.abify.storage.save_experiment({
            'name': self.name
            'splits': [x.to_dict() for x in self.splits]
        })

    def __enter__(self):
        """ Enters a `with` block, which triggers the experiment """
        return self._run_experiment()

    def _run_experiment(self):
        """
        Runs the split test.

        If the user is not participating, one of the splits is selected and registered in the user's session.
        Otherwise, the user is given the split he belongs to.
        """
        if self._user_eligable():
            split = self.recover_split() or self.store_split(self.random_split())
        else:
            # User is not eligable, so just use the control split
            split = self.splits[0]

    def recover_split(self):
        """ Recovers a previously selected split, iff there is one """
        if self.name in self.abify.session:
            return _split_from_session()

    def _split_from_session(self):
        split = filter(lambda x: x == self.abify.session[self.name], self.splits)
        # If we found the split (still active), then we can re-use it, otherwise we are consfused and 
        # disregard the whole old thing.
        if len(split) == 1:
            return split[0]

    def store_split(self, split):
        if self.name in self.abify.session:
            old_split = _split_from_session
            if old_split:
                old_split.decrease()

        split.increase()
        self.abify.session[self.name] = split
