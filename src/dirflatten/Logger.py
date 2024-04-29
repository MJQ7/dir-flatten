from rich.panel import Panel

class Logger():

    LOG = []
    DISPLAYED_LOG = "\n".join(LOG[-30:])
    LAYOUT = None

    @classmethod
    def create(self, layout):
        self.LAYOUT = layout
        Logger.write(self, "[cyan]Starting...")

    @classmethod
    def update(self):
        self.DISPLAYED_LOG = "\n".join(Logger.LOG[-30:])
        self.LAYOUT['log'].update(Panel(self.DISPLAYED_LOG, title="Logs"))
        
    def write(self, entry):
        Logger.LOG.append(entry)
        Logger.update()
