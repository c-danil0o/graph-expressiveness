from api.src.services.source_plugin import SourcePlugin


class EthereumDatasource(SourcePlugin):
    def load(self):
        pass

    def identifier(self):
        return "graph-explorer-ethereum-datasource"

    def name(self):
        return "ethereum_datasource"