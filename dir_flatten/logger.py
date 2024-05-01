from rich.panel import Panel

class Logger():
    _instance = None
    LOG = []
    DISPLAYED_LOG = "\n".join(LOG[-30:])
    LAYOUT = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = Logger()
        return cls._instance

    @classmethod
    def create(cls, layout):
        cls.LAYOUT = layout
        cls.write("[cyan]Starting...")

    @classmethod
    def update(cls):
        cls.DISPLAYED_LOG = "\n".join(cls.LOG[-30:])
        cls.LAYOUT['log'].update(Panel(cls.DISPLAYED_LOG, title="Logs"))

    @classmethod
    def write(cls, entry):
        cls.LOG.append(entry)
        cls.update()
