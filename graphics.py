import svgwrite
from svgwrite.shapes import Line
from random import randint
import os

def save_svg(filename, map, tracks=[], grade="", border=5, out_directory="out"):
    """
    Saves a graphical representation of the map to a SVG file.

    filename: the name of the SVG file
    map: map object which should be saved
    tracks: optional track objects which should also be saved
    border: how big the border should be
    out_directory: folder in which to save the SVG file
    """
    # create out directory if it doesn't exist
    if not os.path.exists(out_directory):
        os.makedirs(out_directory)
    svg = svgwrite.Drawing(out_directory + "/" + filename)
    # get dimensions of the map
    max_x = 0
    max_y = 0
    for line in map.map:
        max_x = max(max_x, max(line[0].x, line[1].x))
        max_y = max(max_y, max(line[0].y, line[1].y))
    # background
    svg.add(svg.rect((0,0), (max_x+2*border, max_y+2*border), fill="white"))
    # paint walls
    walls = svg.add(svg.g(id="walls", stroke="red"))
    for line in map.map:
        p = (line[0].x + border, line[0].y + border)
        q = (line[1].x + border, line[1].y + border)
        walls.add(svg.line(p, q))
    # paint start
    start_x, start_y = map.start
    svg.add(svg.circle((start_x + border, start_y + border), 2, fill="green"))
    # paint target
    target_x, target_y = map.target
    svg.add(svg.circle((target_x + border, target_y + border), 2, fill="blue"))
    # paint tracks
    for i, track in enumerate(tracks):
        id = "track_{:010d}".format(i)
        color = "rgb({:3d},{:3d},{:3d})".format(randint(0, 255),
                                                randint(0, 255),
                                                randint(0, 255))
        svg_track = svg.add(svg.g(id=id, stroke=color))
        for i in range(1, len(track.positions)):
            # ensure that the tracks end at the border
            p_x = min(max_x + 2 * border, track.positions[i-1].x + border)
            p_x = max(p_x, 0)
            p_y = min(max_y + 2 * border, track.positions[i-1].y + border)
            p_y = max(p_y, 0)
            q_x = min(max_x + 2 * border, track.positions[i].x + border)
            q_x = max(q_x, 0)
            q_y = min(max_y + 2 * border, track.positions[i].y + border)
            q_y = max(q_y, 0)
            svg_track.add(svg.line((p_x, p_y), (q_x, q_y)))
    if grade:
        string = "Grade: {:3.2f}".format(grade)
        svg.add(svg.text(string, insert=(0.6*max_x, 0.2*max_y), fill="black", style="font-size:8"))
    svg.save()
