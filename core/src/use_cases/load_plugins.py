from importlib.metadata import entry_points
import typing


source_entry_points = entry_points(group='graph.sources')
visualizer_entry_points = entry_points(group='graph.visualizers')

source_plugins: list[str] = []
visualizer_plugins: list[str] = []


def load_plugins():
    for entry_point in source_entry_points:
        plugin = entry_point.load()
        source_plugins.append(plugin.DataSource())

    for entry_point in visualizer_entry_points:
        plugin = entry_point.load()
        visualizer_plugins.append(plugin.Visualizer())


def get_visualizer_plugins():
    return visualizer_plugins


def get_source_plugins():
    return source_plugins
