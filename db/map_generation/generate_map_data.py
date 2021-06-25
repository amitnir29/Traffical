from db.map_generation.graphs.graph import Graph
from db.map_generation.new_dir_creation import create_new_dir
from db.map_generation.save_to_files import save_junctions


def generate_map(width, height):
    path = create_new_dir()
    g = Graph(width, height)
