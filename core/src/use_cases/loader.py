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
    a = {'blocks_num': 2, 'graph_name': 'asd', 'latest_block': -1, 'depth': 2}


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

    def load_graph(self, source_plugin_id: int) -> Graph:
        self.loaded_graphs[source_plugin_id] = self.sources[source_plugin_id].plugin.load(self.a)
        return self.loaded_graphs[source_plugin_id]

    def get_sources(self) -> list[Plugin]:
        return self.sources

    def get_visualizers(self) -> list[Plugin]:
        return self.visualizers

    def get_loaded_graph(self, plugin: int) -> Graph:
        if plugin in self.loaded_graphs.keys():
            return self.loaded_graphs[plugin]
        else:
            return self.load_graph(plugin)
