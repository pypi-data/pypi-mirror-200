from __future__ import annotations
from pathlib import Path

from pybi.core import DataSource
import pandas as pd

from typing import TYPE_CHECKING, Dict, List, Optional, Union
import os

from pybi.core.components import (
    ContainerComponent,
    ColBoxComponent,
    ComponentTag,
    BoxComponent,
    FlowBoxComponent,
    TextComponent,
    UploadComponent,
    GridBoxComponent,
    TabsComponent,
    Markdown,
    IconComponent,
    AffixComponent,
    Mermaid,
)
from pybi.core.components.reactiveComponent import EChart, Slicer, Table, TextValue
from pybi.core.dataSource import (
    DataSourceField,
    DataSourceTable,
    DataView,
    DataViewBase,
    PivotDataView,
)
from pybi.utils.dataSourceUtils import ds2sqlite_file_base64, ds2sqlite
from pybi.utils.data_gen import (
    JsonUtils,
    random_ds_name,
    random_dv_name,
    get_project_root,
)
from pybi.utils.markdown2 import markdown
from pybi.core.uiResource import ResourceManager

from pybi.core.sql import SqlInfo, SqlWrapper
import pybi.utils.sql as sqlUtils
from pybi.easyEcharts.base import BaseChart, ChartCollector
from pybi.easyEcharts import easy_echarts
from pybi.core.components.reactiveComponent.echarts import (
    EChartInfo,
    EChartDatasetInfo,
    EChartJscode,
    OptionsExtractor,
)
import pybi.utils.pyecharts_utils as pyecharts_utils

if TYPE_CHECKING:
    pass
    # from pybi.core.components import ReactiveComponent


class AppMeta:
    def __init__(self, app: App) -> None:
        self.__app = app

    def set_dbLocalStorage(self, on: bool):
        """
        是否开启数据库本地缓存
        """
        self.__app.dbLocalStorage = on
        return self

    def set_echarts_renderer(self, renderer="canvas"):
        """
        echarts renderer type: 'canvas' or 'svg'
        'canvas' is default
        """
        self.__app.echartsRenderer = renderer
        return self

    def set_doc_title(self, title: str):
        self.__app._doc_title = title
        return self


class App(ContainerComponent):
    def __init__(self) -> None:
        super().__init__(ComponentTag.App)
        self.dataSources: List[DataSource] = []
        self.dataViews: List[DataViewBase] = []
        self.__dataSetNames = set()
        self._with_temp_host_stack: List[ContainerComponent] = []
        self._clear_data = False
        self.dbLocalStorage = False
        self.echartsRenderer = "canvas"
        self._doc_title = None
        self.__meta = AppMeta(self)
        self.__json_utils = JsonUtils()
        self.__resourceManager = ResourceManager()

    def __record_and_check_dataset_name(self, name: str):
        if name in self.__dataSetNames:
            raise Exception(f"dataset name '{name}' is duplicate")
        self.__dataSetNames.add(name)

    @property
    def meta(self):
        return self.__meta

    def clear_all_data(self):
        self._clear_data = True

    def _get_temp_host(self):
        if self._with_temp_host_stack:
            return self._with_temp_host_stack[len(self._with_temp_host_stack) - 1]
        return None

    def set_source(self, data: pd.DataFrame, *, name: Optional[str] = None):
        name = name or random_ds_name()
        self.__record_and_check_dataset_name(name)

        ds = DataSource(name, data)
        self.dataSources.append(ds)
        return DataSourceTable(ds.name, data.columns.tolist(), host=self)

    def set_dataView(
        self,
        sql: str,
        exclude_source: Optional[List[DataSourceTable]] = None,
        *,
        name: Optional[str] = None,
    ):
        exclude_source = exclude_source or []
        name = name or random_dv_name()
        self.__record_and_check_dataset_name(name)
        dv = DataView(name, sql)

        for es in exclude_source:
            dv.exclude_source(es.source_name)

        self.dataViews.append(dv)
        return DataSourceTable(
            dv.name, sqlUtils.extract_fields_head_select(sql), host=self
        )

    def set_pivot_dataView(
        self,
        source: str,
        row: str,
        column: str,
        cell: str,
        agg="min",
        exclude_source: Optional[List[DataSourceTable]] = None,
        excludeRowFields=False,
        *,
        name: Optional[str] = None,
    ):
        exclude_source = exclude_source or []
        name = name or random_dv_name()
        self.__record_and_check_dataset_name(name)
        pdv = PivotDataView(name, source, row, column, cell, agg, excludeRowFields)

        for es in exclude_source:
            pdv.exclude_source(es.source_name)

        self.dataViews.append(pdv)
        return DataSourceTable(pdv.name, [], host=self)

    def sql(self, sql: str):
        return SqlWrapper(sql)

    def add_upload(
        self,
        *,
        host: Optional[ContainerComponent] = None,
    ):

        cp = UploadComponent()

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        self.__resourceManager.register_element_cps()
        return cp

    def add_text(
        self,
        text: Union[str, SqlWrapper],
        *,
        host: Optional[ContainerComponent] = None,
    ):
        if isinstance(text, SqlWrapper):
            text = str(text)
        contexts = list(SqlInfo.extract_sql_from_text(text))

        cp = TextValue(contexts)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def add_slicer(
        self,
        field: Union[DataSourceField, DataSourceTable],
        *,
        orderby: Optional[str] = None,
        host: Optional[ContainerComponent] = None,
    ):
        """
        orderby:
            Defaults `None`:  select distinct colA from data
            '1' : select distinct colA from data order by 1
            '1 desc' : select distinct colA from data order by 1 desc
            'colX dsce' : select distinct colA from data order by colX desc
        """
        if isinstance(field, DataSourceTable):
            field = field[field.columns[0]]

        assert isinstance(field, DataSourceField)
        orderSql = "" if orderby is None else f"order by {orderby}"
        sql = f"select distinct {field._get_sql_field_name()} from {field.source_name} {orderSql}"
        cp = Slicer(SqlInfo(sql))
        cp.title = field.name
        cp.add_updateInfo(field.source_name, field._get_sql_field_name())

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        self.__resourceManager.register_element_cps()
        return cp

    def add_table(
        self,
        dataSourceTable: DataSourceTable,
        *,
        host: Optional[ContainerComponent] = None,
    ):

        sql = ""
        if dataSourceTable._user_specified_field:
            sql = dataSourceTable._to_sql()
        else:
            sql = f"select * from {dataSourceTable.source_name}"
        cp = Table(SqlInfo(sql))

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        self.__resourceManager.register_element_cps()
        return cp

    def add_echart(
        self,
        options: Union[Dict, BaseChart, ChartCollector],
        *,
        host: Optional[ContainerComponent] = None,
    ):
        cp = None

        if not isinstance(options, (BaseChart, ChartCollector, dict)):
            from pyecharts.charts.base import Base

            if isinstance(options, Base):
                options = options.get_options()
                assert isinstance(options, dict)
                pyecharts_utils.replace_jscode(options)
                #
                self.__json_utils.mark_pyecharts()

        if isinstance(options, (BaseChart, ChartCollector)):
            opts = options

            if isinstance(opts, BaseChart):
                opts = ChartCollector().append(opts)

            cp = EChart(option_type="dict")

            if (
                len(opts._collector) > 1
                and easy_echarts._settings.drill_down_default_set_click_filter
            ):
                for chart in opts._collector:
                    chart._create_default_click_filter()

            for chart in opts._collector:
                opts, updateInfos = chart.get_options_infos()

                ds_infos = []
                jscodes = []

                OptionsExtractor.extract_and_remove_from_dict(opts, ds_infos, jscodes)

                ds_infos = [
                    EChartDatasetInfo({}, path, sql._sql_info) for path, sql in ds_infos
                ]

                jscodes = [EChartJscode(path, jscode) for path, jscode in jscodes]

                info = EChartInfo(opts, ds_infos, updateInfos, jscodes)
                cp._add_chart_info(info)

        elif isinstance(options, dict):
            cp = EChart(option_type="dict")

            ds_infos = []
            jscodes = []

            OptionsExtractor.extract_and_remove_from_dict(options, ds_infos, jscodes)

            ds_infos = [
                EChartDatasetInfo({}, path, sql._sql_info) for path, sql in ds_infos
            ]

            jscodes = [EChartJscode(path, jscode) for path, jscode in jscodes]

            info = EChartInfo(options, ds_infos, [], jscodes)
            cp._add_chart_info(info)

        host = host or self._get_temp_host() or self

        assert cp is not None
        host._add_children(cp)

        self.__resourceManager.register_echarts()
        return cp

    def flowBox(
        self,
        *,
        host: Optional[ContainerComponent] = None,
    ):
        cp = FlowBoxComponent(self)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def gridBox(
        self,
        areas: Union[List[List[str]], str],
        *,
        host: Optional[ContainerComponent] = None,
    ):
        if isinstance(areas, str):
            areas = GridBoxComponent.areas_str2array(areas)

        cp = GridBoxComponent(areas, self)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def colBox(
        self,
        spec: List[int] | None = None,
        *,
        host: Optional[ContainerComponent] = None,
    ):
        cp = ColBoxComponent(spec, self)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def box(
        self,
        *,
        host: Optional[ContainerComponent] = None,
    ):
        cp = BoxComponent(self)
        host = host or self._get_temp_host() or self
        host._add_children(cp)
        return cp

    def add_tabs(
        self,
        names: List[str],
        *,
        host: Optional[ContainerComponent] = None,
    ):
        """ """
        cp = TabsComponent(names, appHost=self)
        host = host or self._get_temp_host() or self
        host._add_children(cp)

        self.__resourceManager.register_element_cps()
        return cp

    def save_zip_db(self, path: str):
        with open(path, mode="w", encoding="utf8") as f:
            f.write(ds2sqlite_file_base64(self.dataSources))

    def save_db(self, path: str):
        if Path(path).exists():
            os.remove(path)
        ds2sqlite(path, self.dataSources)

    def _to_json_dict(self):
        data = super()._to_json_dict()

        data["dbFile"] = ds2sqlite_file_base64(
            self.dataSources, clear_data=self._clear_data
        )
        if self._doc_title:
            data["docTitle"] = self._doc_title
        return data

    def __reset_data(self):
        """support for run on ipython env"""
        self.children = []
        self.dataSources = []
        self.dataViews = []

    def to_json(self, *args, **kws):
        return self.__json_utils.dumps(self, *args, **kws)
        # return json_dumps_fn(self, indent=2, ensure_ascii=False)

    def to_raw_html(self):
        try:
            symbol = '"__{{__config_data__}}___"'

            config = self.__json_utils.dumps(self)

            with open(
                get_project_root() / "template/index.html", mode="r", encoding="utf8"
            ) as html:
                res = html.read().replace(symbol, config)
                return res
        except Exception as e:
            raise e
        else:
            self.__reset_data()

    def to_html(self, file, display_output_path=False):
        try:
            # file = Path(file)
            # raw = self.to_raw_html()

            raw = self.__resourceManager.build_html(self.to_json())
            Path(file).write_text(raw, "utf8")

            if display_output_path:
                print(f"to html:{file.absolute()}")
        except Exception as e:
            raise e
        else:
            self.__reset_data()

    def add_markdown(
        self,
        md: str,
        *,
        host: Optional[ContainerComponent] = None,
    ):
        # if isinstance(md, SqlWrapper):
        #     md = str(md)
        md = SqlInfo.around_backticks(md)

        html = markdown(
            md,
            extras=[
                "fenced-code-blocks",
                "target-blank-links",
                "task_list",
                "code-color",
                "tag-friendly",
            ],
        )

        contents = list(SqlInfo.extract_sql_from_text(html))

        cp = Markdown(contents)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def add_icon(
        self,
        svg: str,
        size="2em",
        color="currentColor",
        *,
        host: Optional[ContainerComponent] = None,
    ):

        cp = IconComponent(svg, size, color)

        host = host or self._get_temp_host() or self
        host._add_children(cp)

        return cp

    def affix(
        self,
        *,
        host: Optional[ContainerComponent] = None,
    ):
        cp = AffixComponent(self)
        host = host or self._get_temp_host() or self
        host._add_children(cp)

        self.__resourceManager.register_element_cps()
        return cp

    def add_mermaid(
        self,
        graph: str,
        *,
        host: Optional[ContainerComponent] = None,
    ):
        """
        [mermaid文档](https://github.com/mermaid-js/mermaid/blob/develop/README.zh-CN.md)
        ---
        >>> graph = '''
        flowchart LR
        A[Hard] -->|Text| B(Round)
        B --> C{Decision}
        C -->|One| D[Result 1]
        C -->|Two| E[Result 2]
        '''
        >>> add_mermaid(graph)
        """
        cp = Mermaid(graph)
        host = host or self._get_temp_host() or self
        host._add_children(cp)

        self.__resourceManager.register_mermaid_cps()
        return cp
