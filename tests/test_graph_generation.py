# -*- coding: utf-8 -*-
import unittest
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.actinia_processing.base import ProcessNode, ProcessGraph

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

graph_filter_bbox_nc_legacy = {
    "process_graph": {
        "process_id": "filter_bbox",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.PERMANENT.raster.elevation"
        },
        "spatial_extent": {
            "left": -40.5,
            "right": 75.5,
            "top": 75.5,
            "bottom": 25.25,
            "width_res": 0.1,
            "height_res": 0.1,
        }
    }
}


graph_filter_bbox_nc = {
  "title": "Bounding box filtering of raster layer elevation",
  "description": "This process graph applies the bounding box filter to a raster layer",
  "process_graph": {
    "filter_bbox_1": {
      "process_id": "filter_bbox",
      "arguments": {
        "data": {"from_node": "get_data_1"},
        "left": -40.5,
        "right": 75.5,
        "top": 75.5,
        "bottom": 25.25,
        "width_res": 0.1,
        "height_res": 0.1,
      }
    },
    "get_data_1": {
      "process_id": "get_data",
      "arguments": {
        "data": {
          "name": "nc_spm_08.PERMANENT.raster.elevation"
        }
      }
    }
  }
}

graph_ndvi_strds_legacy = {
    "process_graph": {
        "process_id": "NDVI",
        "red": "lsat5_red",
        "nir": "lsat5_nir",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.landsat.strds.lsat5_red",
            "imagery": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.landsat.strds.lsat5_nir"
            }
        }
    }
}

graph_ndvi_strds = {
  "title": "Compute the NDVI based on two STRDS",
  "description": "Compute the NDVI data from two space-time raster datasets",
  "process_graph": {
    "ndvi_1": {
      "process_id": "NDVI",
      "arguments": {
        "red": {"from_node": "get_red_data"},
        "nir": {"from_node": "get_nir_data"},
      }
    },
    "get_red_data": {
      "process_id": "get_data",
      "arguments": {
        "data": {
          "name": "nc_spm_08.landsat.strds.lsat5_red"
        }
      }
    },
    "get_nir_data": {
      "process_id": "get_data",
      "arguments": {
        "data": {
          "name": "nc_spm_08.landsat.strds.lsat5_nir"
        }
      }
    }
  }
}

graph_use_case_1 = {
    "process_graph": {
        "process_id": "reduce_time",
        "method": "minimum",
        "imagery": {
            "process_id": "NDVI",
            "red": "lsat5_red",
            "nir": "lsat5_nir",
            "imagery": {
                "process_id": "filter_daterange",
                "from": "2001-01-01",
                "to": "2005-01-01",
                "imagery": {
                    "process_id": "filter_bbox",
                    "imagery": {
                        "process_id": "get_data",
                        "data_id": "nc_spm_08.landsat.strds.lsat5_red",
                        "imagery": {
                            "process_id": "get_data",
                            "data_id": "nc_spm_08.landsat.strds.lsat5_nir",
                        }
                    },
                    "spatial_extent": {
                        "left": -40.5,
                        "right": 75.5,
                        "top": 75.5,
                        "bottom": 25.25,
                        "width_res": 0.1,
                        "height_res": 0.1,
                    }
                }
            }

        }
    }
}


example_graph = {
  "title": "NDVI based on Sentinel 2",
  "description": "Deriving minimum NDVI measurements over pixel time series of Sentinel 2",
  "process_graph": {
    "export1": {
      "process_id": "export",
      "arguments": {
        "data": {
          "from_node": "mergec1"
        },
        "format": "png"
      }
    },
    "export2": {
      "process_id": "export",
      "arguments": {
        "data": {
          "from_node": "reduce2"
        },
        "format": "png"
      },
      "result": True
    },
    "filter1": {
      "process_id": "filter_temporal",
      "arguments": {
        "data": {
          "from_node": "getcol1"
        },
        "from": "2017-01-01",
        "to": "2017-01-31"
      }
    },
    "filter2": {
      "process_id": "filter_temporal",
      "arguments": {
        "data": {
          "from_node": "getcol1"
        },
        "from": "2018-01-01",
        "to": "2018-01-31"
      }
    },
    "filter3": {
      "process_id": "filter_bands",
      "arguments": {
        "bands": [
          "nir",
          "red"
        ],
        "data": {
          "from_node": "reduce1"
        }
      }
    },
    "getcol1": {
      "process_id": "get_collection",
      "arguments": {
        "name": "Sentinel-1"
      }
    },
    "mergec1": {
      "process_id": "merge_collections",
      "arguments": {
        "data1": {
          "from_node": "filter1"
        },
        "data2": {
          "from_node": "filter2"
        }
      }
    },
    "reduce1": {
      "process_id": "reduce",
      "arguments": {
        "data": {
          "from_node": "mergec1"
        },
        "dimension": "temporal",
        "reducer": {
          "callback": {
            "min1": {
              "process_id": "min",
              "arguments": {
                "data": {
                  "from_argument": "dimension_data"
                },
                "dimension": {
                  "from_argument": "dimension"
                }
              },
              "result": True
            }
          }
        }
      }
    },
    "reduce2": {
      "process_id": "reduce",
      "arguments": {
        "data": {
          "from_node": "filter3"
        },
        "dimension": "spectral",
        "reducer": {
          "callback": {
            "divide1": {
              "process_id": "divide",
              "arguments": {
                "x": {
                  "from_node": "substr1"
                },
                "y": {
                  "from_node": "sum1"
                }
              },
              "result": True
            },
            "output1": {
              "process_id": "output",
              "arguments": {
                "data": {
                  "from_node": "divide1"
                }
              }
            },
            "substr1": {
              "process_id": "substract",
              "arguments": {
                "data": {
                  "from_argument": "dimension_data"
                }
              }
            },
            "sum1": {
              "process_id": "sum",
              "arguments": {
                "data": {
                  "from_argument": "dimension_data"
                }
              }
            }
          }
        }
      }
    }
  }
}


class GraphValidationTestCase(TestBase):

    def test_graph_creation_example_graph(self):

        pg = ProcessGraph(example_graph)
        print(pg.root_nodes)

        self.assertEqual(2, len(pg.root_nodes))
        self.assertEqual(9, len(pg.node_dict))

    def test_graph_creation_graph_filter_bbox_nc(self):
        pg = ProcessGraph(graph_filter_bbox_nc)
        print(pg.root_nodes)

        self.assertEqual(1, len(pg.root_nodes))
        self.assertEqual(2, len(pg.node_dict))

    def test_graph_creation_graph_graph_ndvi_strds(self):

        pg = ProcessGraph(graph_ndvi_strds)
        print(pg.root_nodes)

        self.assertEqual(1, len(pg.root_nodes))
        self.assertEqual(3, len(pg.node_dict))

        print(pg.node_dict)
        print(pg.node_dict["ndvi_1"])


if __name__ == "__main__":
    unittest.main()