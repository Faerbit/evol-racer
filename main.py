#!/usr/bin/env python3

import argparse
import configparser
import os
import sys
from map import Map
from population import Population
from graphics import save_svg
from contexttimer import Timer
from collections import deque
from ast import literal_eval

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
        self.grade = 0
        self.grades = []

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
            string = ("\r" + msg + "{:>" + str(120 - len(msg))
                    + "s}\n").format("[\033[32mOK\033[0m]")
            sys.stdout.write(string)
        sys.stdout.flush()

    def status_msg(self, timestep, writing):
        """Convenience function for status messages."""
        timestep_mean = float(self.timestep_durations.average)
        write_mean    = float(self.write_durations.average)
        string = ("\rCurrent timestep: {:>" + str(len(str(self.max_timesteps)) + 2) +
                  "d} -- Grade: {:>5.2f} -- {:>3.5f}s per Gen. "
                  "-- {:>3.5f}s per file").format(timestep, self.grade, timestep_mean, write_mean)
        if not writing:
            sys.stdout.write("{:120s}".format(string))
        else:
            sys.stdout.write("{:120s}".format(string + "\033[5m ... writing file ...\033[0m"))
        sys.stdout.flush()


    def filename(self, timestep):
        """Picks the right filename for the SVG file"""
        return ("test_{:0" + str(len(str(self.max_timesteps))) + "d}.svg").format(timestep)


    def save(self, timestep, map, tracks):
        """Saves plot of current population."""
        self.status_msg(timestep, writing=True)
        if self.grade != 0:
            grade = self.grade
        else:
            grade = ""
        with Timer() as write_timer:
            save_svg(self.filename(timestep), map, tracks, grade, out_directory=self.out_directory)
        write_duration = write_timer.elapsed
        self.write_durations.append(write_duration)
        self.status_msg(timestep, writing=False)

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

            write_plots = literal_eval(config["Plots"]["enabled"])
            self.out_directory = config["Plots"]["out_directory"]
            write_frequency = int(config["Plots"]["frequency"])
            clean_previous = literal_eval(config["Plots"]["clean_previous"])
            plot_grades = literal_eval(config["Plots"]["plot_grades"])
        else:
            raise Exception("Config file " + args.config_file + " not found. Exiting.")

        self.init_msg("Reading config ...", ok=True)
        if clean_previous and os.path.exists(self.out_directory):
            self.init_msg("Cleaning previous plots ...", ok=False)
            os.system("rm -rf " + self.out_directory + "/*")
            self.init_msg("Cleaning previous plots ...", ok=True)

        map = Map(max_acceleration, map_file_name)
        if write_plots:
            self.init_msg("Saving map ...", ok=False)
            save_svg("map.svg", map, out_directory=self.out_directory)
            self.init_msg("Saving map ...", ok=True)
        self.init_msg("Generating population ...", ok=False)
        population = Population(
                map=map,
                population_size=population_size,
                distance_factor=distance_factor,
                collision_penalty=collision_penalty,
                retain_percentage=retain_percentage,
                random_select_chance=random_select_chance,
                mutate_chance=mutate_chance)
        self.init_msg("Generating population ...", ok=True)
        # write first plot
        if write_plots:
            self.save(0, map, population.tracks)
        for i in range(1, self.max_timesteps + 1):
            self.status_msg(i, writing=False)
            with Timer() as timer:
                self.grade = population.evolve()
            # write plots regularly
            self.grades.append((i, self.grade))
            if (write_plots and i % write_frequency == 0):
                self.save(i, map, population.tracks)
            self.timestep_durations.append(timer.elapsed)

        # write final plot
        if (write_plots and not (i % write_frequency == 0)):
            self.save(i, map, population.tracks)

        if plot_grades:
            with open(self.out_directory + "/grades", "w") as grade_file:
                for timestep, grade in self.grades:
                    string = ("{:>" + str(len(str(self.max_timesteps)))
                            + "} {:>4.5f}\n").format(timestep, grade)
                    grade_file.write(string)
            with open(self.out_directory + "/plot", "w") as plot_file:
                plot_file.write("set term pdf\n")
                plot_file.write("set out '" + self.out_directory + "/grades.pdf'\n")
                plot_file.write("set xlabel 'Timestep'\n")
                plot_file.write("set ylabel ' Grade'\n")
                plot_file.write("p '" + self.out_directory + "/grades' u 1:2 w l title 'Grades'\n")
            os.system("gnuplot " + self.out_directory + "/plot")

if __name__ == "__main__":
    interface = Interface()
    with interface:
        interface.run()
