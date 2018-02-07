# -*- coding: utf-8 -*-
from graas_openeo_core_wrapper import process_definitions

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


PROCESS_NAME = "filter_bbox"

DOC = {
    "process_id": "filter_bbox",
    "description": "Drops observations from a collection that are located outside of a given bounding box.",
    "args": {
        "collections": {
            "description": "array of input collections with one element"
        },
        "left": {
            "description": "left boundary (longitude / easting)"
        },
        "right": {
            "description": "right boundary (longitude / easting)"
        },
        "top": {
            "description": "top boundary (latitude / northing)"
        },
        "bottom": {
            "description": "bottom boundary (latitude / northing)"
        },
        "srs": {
            "description": "spatial reference system of boundaries as proj4 or EPSG:12345 like string"
        }
    }
}

process_definitions.PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_command(input_time_series, output_map):
    """Create a GRaaS process description that uses t.rast.series to create the minimum
    value of the time series.

    :param input_time_series: The input time series name
    :param output_map: The name of the output map
    :return: A GRaaS process chain description
    """

    pc = {"id": "t_rast_series",
          "module": "t.rast.series",
          "inputs": [{"param": "input", "value": input_time_series},
                     {"param": "method", "value": "minimum"},
                     {"param": "output", "value": output_map}],
          "flags": "t"}

    return pc


def get_process_list(leaf):
    """Analyse the process description and return the GRaaS process chain and the name of the processing result layer
    which is a single raster layer

    :param leaf: The process description
    :return: (output_name, pc)
    """
    input_name, process_list = process_definitions.check_leaf(leaf)

    # Create the output name based on the input name and method
    output_name = input_name + "_" + PROCESS_NAME

    pc = create_command(input_name, output_name)
    process_list.append(pc)

    return (output_name, process_list)


process_definitions.PROCESS_DICT[PROCESS_NAME] = get_process_list