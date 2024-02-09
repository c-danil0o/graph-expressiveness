import threading
from importlib.metadata import entry_points

from api.src.types.graph import Graph
from core.src.models.plugin import Plugin


class Loader:
    _instance = None
    _lock = threading.Lock()
    source_entry_points = entry_points(group='graph.sources')
    visualizer_entry_points = entry_points(group='graph.visualizers')
    sources: list[Plugin] = []
    visualizers: list[Plugin] = []
    loaded_graphs: dict[int, Graph] = {}

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

    def load_graph(self, source_plugin_id: int, config) -> Graph:
        key = hash(str(source_plugin_id) + str(config))
        self.loaded_graphs[key] = self.sources[source_plugin_id].plugin.load(config)
        return self.loaded_graphs[key]

    def get_sources(self) -> list[Plugin]:
        return self.sources

    def get_visualizers(self) -> list[Plugin]:
        return self.visualizers

    def is_graph_loaded(self, source_plugin_id: int, config: dict) -> bool:
        return hash(str(source_plugin_id) + str(config)) in self.loaded_graphs.keys()

    def get_loaded_graph(self, plugin: int, config: dict) -> Graph:
        key = hash(str(plugin) + str(config))
        if key in self.loaded_graphs.keys():
            return self.loaded_graphs[key]
        else:
            return self.load_graph(plugin, config)

    def get_settings(self, plugin: int):
        return self.sources[plugin].plugin.params()
