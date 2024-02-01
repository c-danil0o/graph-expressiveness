class Plugin(object):
    def __init__(self, plugin, plugin_id: int, description: str = ''):
        self.plugin = plugin
        self.plugin_id = plugin_id
        self.description = description
