from db.map_generation.graphs.graph import Graph
from db.map_generation.new_dir_creation import create_new_dir
from db.pickle_help import jsonpickle_to_file


def generate_map(width, height, lane_length=10):
    """
    generate a new map and save it to the db.
    :param width: width of the 2d array of junctions
    :param height: height of the 2d array of junctions
    :param lane_length: sets the length of the lanes, relatively
    """
    path = create_new_dir()
    g = Graph(width, height, lane_length=lane_length, juncs_dist=20)
    roads_data, juncs_data = g.build_map(with_tests=True, with_prints=False)
    jsonpickle_to_file(roads_data, path + "/" + "RoadSections.json")
    jsonpickle_to_file(juncs_data, path + "/" + "Junctions.json")
