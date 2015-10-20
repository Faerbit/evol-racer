import svgwrite
from svgwrite.shapes import Line
from random import randint
import os

def save_svg(filename, map, tracks=[], offset=5, out_directory="out"):
    """ Saves a graphical representation of the map to a SVG file. """
    if not os.path.exists(out_directory):
        os.makedirs(out_directory)
    svg = svgwrite.Drawing(out_directory + "/" + filename)
    # get dimensions
    max_x = 0
    max_y = 0
    for line in map.map:
        max_x = max(max_x, max(line[0].x, line[1].x))
        max_y = max(max_y, max(line[0].y, line[1].y))
    # background
    svg.add(svg.rect((0,0), (max_x+2*offset, max_y+2*offset), fill="white"))
    walls = svg.add(svg.g(id="walls", stroke="red"))
    for line in map.map:
        p = (line[0].x + offset, line[0].y + offset)
        q = (line[1].x + offset, line[1].y + offset)
        walls.add(svg.line(p, q))
    start_x, start_y = map.start
    svg.add(svg.circle((start_x + offset, start_y + offset), 2, fill="green"))
    target_x, target_y = map.target
    svg.add(svg.circle((target_x + offset, target_y + offset), 2, fill="blue"))
    for i, track in enumerate(tracks):
        id = "track_{:010d}".format(i)
        color = "rgb({:3d},{:3d},{:3d})".format(randint(0, 255),
                                                randint(0, 255),
                                                randint(0, 255))
        svg_track = svg.add(svg.g(id=id, stroke=color))
        for i in range(1, len(track.positions)):
            p_x = min(max_x + offset, track.positions[i-1].x + offset)
            p_x = max(p_x, 0)
            p_y = min(max_y + offset, track.positions[i-1].y + offset)
            p_y = max(p_y, 0)
            q_x = min(max_x + offset, track.positions[i].x + offset)
            q_x = max(q_x, 0)
            q_y = min(max_y + offset, track.positions[i].y + offset)
            q_y = max(q_y, 0)
            svg_track.add(svg.line((p_x, p_y), (q_x, q_y)))
    svg.save()
