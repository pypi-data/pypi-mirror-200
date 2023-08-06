from __future__ import annotations
from .line import LineChart
from .bar import BarChart
from .pie import PieChart
from .scatter import ScatterChart
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from pybi.core.dataSource import DataSourceTable


__all__ = ["easy_echarts"]


class EasyEChartsSettings:
    def __init__(self) -> None:
        self.drill_down_default_set_click_filter = True


class EasyEChartsMeta:
    def __init__(self) -> None:
        self._settings = EasyEChartsSettings()

    def off_drill_down_default_set_click_filter(self):
        """
        默认情况下,多个组合图表配置会自动为其每个图表添加 `click_filter` 联动。
        此函数调用后,会关闭其功能
        """
        self._settings.drill_down_default_set_click_filter = False

    def make_line(
        self,
        data: DataSourceTable,
        x: str,
        y: str,
        color: Optional[str] = None,
        agg="round(avg(${}),2)",
    ):
        return LineChart(data, x, y, color, agg)

    def make_bar(
        self,
        data: DataSourceTable,
        *,
        x: str,
        y: str,
        color: Optional[str] = None,
        agg="round(avg(${}),2)",
    ):
        return BarChart(data, x, y, color, agg)

    def make_pie(
        self,
        data: DataSourceTable,
        *,
        name: str,
        value: str,
        agg="round(avg(${}),2)",
    ):
        return PieChart(data, name, value, agg)

    def make_scatter(
        self,
        data: DataSourceTable,
        *,
        x: str,
        y: str,
        color: Optional[str] = None,
        agg="round(avg(${}),2)",
    ):
        return ScatterChart(data, x, y, color, agg)


easy_echarts = EasyEChartsMeta()
