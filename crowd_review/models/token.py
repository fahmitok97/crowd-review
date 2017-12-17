class Token():

    def __init__(self, context='', base_context=''):
        self.context = context
        self.base_context = base_context
        self.properties = []

    def add_prop(self, property):
        self.properties.append(property)

    def get_prop(self):
        return self.properties

    def get_context(self):
        return self.context

    def get_base_context(self):
        return self.base_context

    def __repr__(self):
        return self.context + ' ' + self.base_context + ' ' + ' '.join(self.properties)