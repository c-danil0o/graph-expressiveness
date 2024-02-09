from api.src.services.source_plugin import SourcePlugin
import typing
from concurrent.futures import ThreadPoolExecutor
from github import Github

from api.src.types.graph import Graph, Node, Edge
from api.src.types.param import Param

_graph = Graph
access_token = "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"
# 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
# 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 moj
user_info_cache = {}

new_users = []
last_users = []


def get_user_info(person):
    name = person.login
    if name in user_info_cache:
        return user_info_cache[name]
    user_info = {
        "login": name,
        "email": str(person.email),
        "name": str(person.name),
        "bio": str(person.bio),
        "repos": int(person.public_repos)
    }

    user_info_cache[name] = user_info
    return user_info


def fetch_user_info_parallel(following_user, node):
    if _graph.get_node_count()>200:
        return
    user_info = get_user_info(following_user)
    new_users.append(following_user)
    new_node = Node(user_info["login"], {
        "email": user_info["email"],
        "name": user_info["name"],
        "bio": user_info["bio"],
        "repos": user_info["repos"]
    })
    _graph.add_node(new_node)
    _graph.add_edge(Edge("following", {}, node, new_node, False))


def populate_graph(depth: int):
    print('qm')

    if depth == 0:
        last_users.clear()
        new_users.clear()
        user_info_cache.clear()
        return _graph
    else:
        depth = depth-1
        old_nodes = _graph.nodes.copy()
        with ThreadPoolExecutor() as executor:
            futures = []
            for user in last_users:
                for following_user in user.get_following():
                    if _graph.get_node_count() >= 200:
                        break
                    futures.append(executor.submit(fetch_user_info_parallel, following_user, _graph.get_node(user.login)))
            for future in futures:
                future.result()
        last_users.clear()
        last_users.extend(new_users)
        new_users.clear()
        return populate_graph(depth)


def load_graph(graph_name: str, depth: int, input_access_token: str = "") -> Graph:
    global access_token, _graph
    _graph = Graph('Github', None, [], [])
    if input_access_token is not "":
        access_token = input_access_token

    _graph.name = graph_name
    try:
        login = Github(access_token)
        user = login.get_user()
        root: Node = Node(user.login, {"email": str(user.email), "name": str(user.name), "bio": str(user.bio),
                                       "repos": int(user.public_repos)})
        _graph.set_root(root)
        _graph.add_node(root)
        last_users.append(user)
        return populate_graph(depth)
    except:
        return _graph



class DataSource(SourcePlugin):
    def params(self) -> list[Param]:
        return [Param("Graph name", "graph_name", str), Param("Depth", "depth", int),
                Param("GitHub access token", "access_token", str)]


    def load(self, config: dict):
        return load_graph(config['graph_name'], config["depth"], config["access_token"])

    def identifier(self):
        return "graph-explorer-github-datasource"

    def name(self):
        return "github_datasource"
