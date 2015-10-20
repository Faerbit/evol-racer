#!/usr/bin/python3

import argparse
import configparser
import os
from map import Map
from population import Population
from graphics import save_svg

parser = argparse.ArgumentParser(description="Simulates evolution"
                                                " for tracks on a given map.")
parser.add_argument("--config_file", help="file name of the config file",
                    default="default.cfg")
args = parser.parse_args()

print("Reading config ...")
config = configparser.ConfigParser()
if os.path.isfile(args.config_file):
    config.read(args.config_file)
    map_file_name = config["Map"]["filename"]
    population_size = config["Map"]["population_size"]
    max_acceleration = config["Map"]["max_acceleration"]
    distance_factor = config["Map"]["distance_factor"]
    collision_penalty = config["Map"]["collision_penalty"]
    retain_percentage = config["Map"]["retain_percentage"]
    random_select_chance = config["Map"]["random_select_chance"]
    mutate_chance = config["Map"]["mutate_chance"]
    max_timesteps = int(config["Map"]["max_timesteps"])

    write_plots = config["Plots"]["enabled"]
    out_directory = config["Plots"]["out_directory"]
    write_frequency = int(config["Plots"]["frequency"])
else:
    raise Exception("Config file " + args.config_file + " not found. Exiting.")

map = Map(map_file_name)
print("Generating population ...")
population = Population(
        map=map,
        population_size=population_size,
        max_acceleration=max_acceleration,
        distance_factor=distance_factor,
        collision_penalty=collision_penalty,
        retain_percentage=retain_percentage,
        random_select_chance=random_select_chance,
        mutate_chance=mutate_chance)
print("Starting simulation ...")
for i in range(max_timesteps):
    if (write_plots and i % write_frequency == 0):
        filename = ("test_{:0" + str(len(str(max_timesteps))) + "d}.svg").format(i)
        save_svg(filename, map, population.tracks, out_directory=out_directory)
    population.evolve()
