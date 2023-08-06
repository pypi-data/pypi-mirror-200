from pybi.core.components.component import Component
from .componentTag import ComponentTag
import re


class TextComponent(Component):
    def __init__(self, content: str) -> None:
        super().__init__(ComponentTag.Text)
        self.content = content


class UploadComponent(Component):
    def __init__(self) -> None:
        super().__init__(ComponentTag.Upload)


class SvgIconComponent(Component):
    replace_svg_size_pat = re.compile(r"(width|height)=.+?\s", re.I | re.DOTALL)

    def __init__(self, svg: str, size: str, color: str) -> None:
        super().__init__(ComponentTag.SvgIcon)

        svg = SvgIconComponent.replace_svg_size_pat.sub("", svg)
        self.svg = svg
        self.size = size
        self.color = color


class IconComponent(Component):
    def __init__(self, icon_id: str, size: str, color: str) -> None:
        super().__init__(ComponentTag.Icon)

        self.iconID = icon_id
        self.size = size
        self.color = color
