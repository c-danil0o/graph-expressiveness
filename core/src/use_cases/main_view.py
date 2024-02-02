from core.src.use_cases.loader import Loader


class MainView(object):
    def __init__(self):
        self.loader = Loader()
        self.sources = self.loader.sources
        self.visualizers = self.loader.visualizers

    def generate_main_view(self, source_plugin_id: int, visualizer_plugin_id: int):
        return self.visualizers[visualizer_plugin_id].plugin.show(self.loader.get_loaded_graph(source_plugin_id))
