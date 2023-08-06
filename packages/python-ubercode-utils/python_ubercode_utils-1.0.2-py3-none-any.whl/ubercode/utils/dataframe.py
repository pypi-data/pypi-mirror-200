""" common utilities for working with dataframes"""
from typing import Any
from . import logging


# extend the logging to include log.dataframe()
# NOTE: making dataframe type Any, so we don't have to include pandas but intended use is dataframe
# todo: decide if better to include in different install requiring pandas like the requests utils version
class DataframeLogger(logging.ColorLogger):
    def dataframe(self, dataframe: Any,  label: str = None, color: str = "INFO", df_color: str = "ALWAYS") -> None:
        color = DataframeLogger.DEFAULT_COLOR_MAP.get(color, DataframeLogger.DEFAULT_COLOR_MAP["INFO"])
        df_color = DataframeLogger.DEFAULT_COLOR_MAP.get(df_color, DataframeLogger.DEFAULT_COLOR_MAP["ALWAYS"])
        if label:
            self.always(label, color=color)
        # print(dataframe)
        self.always(str(dataframe), color=df_color)
