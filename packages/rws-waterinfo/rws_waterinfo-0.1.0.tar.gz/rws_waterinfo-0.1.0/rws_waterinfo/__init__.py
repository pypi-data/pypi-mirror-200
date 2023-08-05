# -*- coding: utf-8 -*-
"""Documentation about rws_waterinfo"""
# from rws_waterinfo import rws_waterinfo

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "RWS Datalab"
__email__ = "datalab.codebase@rws.nl"
__version__ = "0.1.0"


from rws_waterinfo.rws_waterinfo import (
    get_catalog,
    get_data,
    set_logger,
    update_dataframe,
)

__all__ = ["set_logger" "get_catalog", "get_data", "update_dataframe"]
