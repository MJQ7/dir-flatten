from rich import print
from rich.panel import Panel
from rich.progress import track, Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, ProgressColumn, TimeElapsedColumn
from rich.layout import Layout
from rich.console import Console

class UI():
    
    @classmethod
    def create_ui(cls):
        cls.progress = cls.create_progress_bar()
        cls.layout = cls.create_layout(cls.progress)
        cls.console = Console()
        cls.max_lines = 20

    def create_progress_bar():
        # Define the layout of the progress bar
        return Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            transient=True
        )
    
    def create_layout(progress):
        layout = Layout()
        panel_progress = Panel(progress, title="Progress")
        layout.split(
            Layout(panel_progress, name='progress', size=3),
            Layout(name='log', ratio=1)  # Placeholder for dynamic log updates
        )
        return layout

    def create_console():
        return Console()