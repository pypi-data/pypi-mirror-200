from __future__ import annotations
from typing import Dict, List, Union


def copt2opt_obj(opts: Dict, name: str):
    if name in opts:
        target = opts[name]

        if isinstance(target, list) and len(target) == 0:
            return

        target = target[0] if isinstance(target, list) else target
        target = {**target}
        return target

    return None


def try_del_prop(obj: Dict, name: str):
    if name in obj:
        del obj[name]


def merge_user_options(
    base_opts: Dict,
):
    def update_config(series_config: Dict):
        series = copt2opt_obj(base_opts, "series")
        if series:

            try_del_prop(series, "data")
            try_del_prop(series, "type")

            series_config.update(series)

    def update_axis(options: Dict):
        xAxis = copt2opt_obj(base_opts, "xAxis")
        if xAxis:
            try_del_prop(xAxis, "data")
        yAxis = copt2opt_obj(base_opts, "yAxis")
        if yAxis:
            try_del_prop(yAxis, "data")

        options["xAxis"][0].update(xAxis)
        options["yAxis"][0].update(yAxis)

    def remove_series():
        if "series" in base_opts:
            base_opts["series"] = []

        if "legend" in base_opts:
            if len(base_opts["legend"]) > 0:
                target = base_opts["legend"][0]
                if "data" in target:
                    del target["data"]

    return update_config, update_axis, remove_series
