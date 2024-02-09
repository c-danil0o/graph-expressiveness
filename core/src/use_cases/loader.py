import threading
from importlib.metadata import entry_points
import os
import pickle


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
    source_plugin_names: dict[int, str] = {}

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
            self.source_plugin_names[i] = plugin.DataSource().name()
            self.sources.append(Plugin(plugin.DataSource(), i))
            i += 1
        i = 0
        for entry_point in self.visualizer_entry_points:
            plugin = entry_point.load()
            print(plugin.Visualizer().name())
            self.visualizers.append(Plugin(plugin.Visualizer(), i))
            i += 1

    def load_graph(self, source_plugin_id: int, config) -> Graph:
        file_name = self.create_file_name(source_plugin_id, config)
        file_path = os.path.join("saved_graphs", file_name)
        key = hash(str(source_plugin_id) + str(config))
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                self.loaded_graphs[key] = pickle.load(file)
        else:
            os.makedirs("saved_graphs", exist_ok=True)
            with open(file_path, 'wb') as file:
                graph = self.sources[source_plugin_id].plugin.load(config)
                self.loaded_graphs[key] = graph
                pickle.dump(graph, file)
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

    def create_file_name(self, source_plugin_id, config) -> str:
        file_name: str = self.source_plugin_names[source_plugin_id][:3]
        for value in config.values():
            file_name += str(value)
        file_name += ".pkl"
        return file_name
