class Token():

    def __init__(self, context=''):
        self.context = context
        self.properties = []

    def add_prop(self, property):
        self.properties.append(property)

    def get_prop(self):
        return self.properties

    def get_context(self):
        return self.context

    def __repr__(self):
        return self.context + ' ' + ' '.join(self.properties)