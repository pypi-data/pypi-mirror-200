class CommandBase:
    description = ''
    options = []

    @staticmethod
    def execute(configuration, arguments=None):
        raise NotImplemented
