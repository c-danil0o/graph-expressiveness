from core.src.use_cases.loader import Loader

a = {'blocks_num': 10, 'graph_name': 'asd', 'latest_block': -1}


class MainView(object):
    def __init__(self):
        self.loader = Loader()
        self.sources = self.loader.sources
        self.visualizers = self.loader.visualizers

    def generate_main_view(self, source_plugin_id: int, visualizer_plugin_id: int):
        return self.visualizers[visualizer_plugin_id].plugin.show(self.sources[source_plugin_id].plugin.load(a))
