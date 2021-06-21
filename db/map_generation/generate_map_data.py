from db.map_generation.new_dir_creation import create_new_dir
from db.map_generation.generate_objects import generate_junc
from db.map_generation.save_to_files import save_junctions


def generate_map():
    path = create_new_dir()
    x = generate_junc()
    save_junctions([x], path)
