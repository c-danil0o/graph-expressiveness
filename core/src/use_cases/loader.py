import threading
from importlib.metadata import entry_points

from core.src.models.plugin import Plugin


class Loader:
    _instance = None
    _lock = threading.Lock()
    source_entry_points = entry_points(group='graph.sources')
    visualizer_entry_points = entry_points(group='graph.visualizers')
    sources: list[Plugin] = []
    visualizers: list[Plugin] = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Loader, cls).__new__(cls)
        return cls._instance

    def init(self):
        i = 0
        for entry_point in self.source_entry_points:
            plugin = entry_point.load()
            self.sources.append(Plugin(plugin.DataSource(), i))
            i += 1
        i = 0
        for entry_point in self.visualizer_entry_points:
            plugin = entry_point.load()
            print(plugin.Visualizer().name())
            self.visualizers.append(Plugin(plugin.Visualizer(), i))
            i += 1

    def get_sources(self) -> list[Plugin]:
        return self.sources

    def get_visualizers(self) -> list[Plugin]:
        return self.visualizers
