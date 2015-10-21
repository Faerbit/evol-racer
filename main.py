#!/usr/bin/python3

import argparse
import configparser
import os
import sys
from map import Map
from population import Population
from graphics import save_svg
from shutil import rmtree
from contexttimer import Timer
from collections import deque

class CircularBuffer(deque):
    def __init__(self, size=0):
        super(CircularBuffer, self).__init__(maxlen=size)
    @property
    def average(self):
        if len(self) > 0:
            return sum(self)/len(self)
        else:
            return 0

class Interface():
    """Provides an interface to the simulation."""

    def __init__(self):
        self.timestep_durations = CircularBuffer(10)
        self.write_durations = CircularBuffer(10)

    def __enter__(self):
        """Hides cursor."""
        os.system("setterm -cursor off")

    def __exit__(self, *args):
        """Shows cursor again and writes final newline."""
        os.system("setterm -cursor on")
        sys.stdout.write("\n")

    def init_msg(self, msg, ok):
        """Convenience function for init messages."""
        if not ok:
            sys.stdout.write(msg)
        else:
            string = ("\r" + msg + "{:>" + str(100 - len(msg))
                    + "s}\n").format("[\033[32mOK\033[0m]")
            sys.stdout.write(string)
        sys.stdout.flush()

    def status_msg(self, timestep, writing):
        """Convenience function for status messages."""
        timestep_mean = float(self.timestep_durations.average)
        write_mean    = float(self.write_durations.average)
        string = ("\rCurrent timestep: {:>" + str(len(str(self.max_timesteps)) + 2) +
                  "d} -- {:>3.5f} Gen/s --- {:>3.5f} s per file").format(timestep, timestep_mean, write_mean)
        if not writing:
            sys.stdout.write("{:100s}".format(string))
        else:
            sys.stdout.write("{:100s}".format(string + "\033[5m ... writing file ...\033[0m"))
        sys.stdout.flush()

    def filename(self, timestep):
        """Picks the right filename for the SVG file"""
        return ("test_{:0" + str(len(str(self.max_timesteps))) + "d}.svg").format(timestep)

    def run(self):
        """Runs the simulation."""
        parser = argparse.ArgumentParser(description="Simulates evolution"
                                                        " for tracks on a given map.")
        parser.add_argument("--config_file", help="file name of the config file",
                            default="default.cfg")
        args = parser.parse_args()

        self.init_msg("Reading config ...", ok=False)
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
            self.max_timesteps = int(config["Map"]["max_timesteps"])

            write_plots = config["Plots"]["enabled"]
            out_directory = config["Plots"]["out_directory"]
            write_frequency = int(config["Plots"]["frequency"])
            clean_previous = config["Plots"]["clean_previous"]
        else:
            raise Exception("Config file " + args.config_file + " not found. Exiting.")

        self.init_msg("Reading config ...", ok=True)
        if clean_previous and os.path.exists(out_directory):
            self.init_msg("Cleaning previous plots ...", ok=False)
            rmtree(out_directory)
            self.init_msg("Cleaning previous plots ...", ok=True)

        map = Map(map_file_name)
        self.init_msg("Generating population ...", ok=False)
        population = Population(
                map=map,
                population_size=population_size,
                max_acceleration=max_acceleration,
                distance_factor=distance_factor,
                collision_penalty=collision_penalty,
                retain_percentage=retain_percentage,
                random_select_chance=random_select_chance,
                mutate_chance=mutate_chance)
        self.init_msg("Generating population ...", ok=True)
        for i in range(self.max_timesteps + 1):
            with Timer() as timer:
                write_duration = 0
                # write plots regularly
                if (write_plots and i % write_frequency == 0):
                    with Timer() as write_timer:
                        self.status_msg(i, writing=True)
                        save_svg(self.filename(i), map, population.tracks, out_directory=out_directory)
                    write_duration = write_timer.elapsed
                    self.write_durations.append(write_duration)
                self.status_msg(i,writing=False)
                population.evolve()
            self.timestep_durations.append(timer.elapsed - write_duration)

        # write final plot
        if write_plots:
            save_svg(self.filename(self.max_timesteps), map, population.tracks, out_directory=out_directory)

if __name__ == "__main__":
    interface = Interface()
    with interface:
        interface.run()
