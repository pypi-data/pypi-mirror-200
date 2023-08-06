from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type
from bs4 import BeautifulSoup

from inline_svg.config import Config
from inline_svg.util import (
    info,
    debug,
    get_svg_data,
    get_svg_tag,
    include_assets,
)
import re
from tempfile import TemporaryDirectory

WILDCARD = "*"


class InlineSvgPlugin(BasePlugin):
    config_scheme = (
        ("AltName", Type(str, default=WILDCARD)),
        ("IncludeAssets", Type(bool, default=False)),
        ("AssetDir", Type(str, default="assets/")),
        ("PatchStyle", Type(bool, default=False)),
    )

    def on_config(self, config, **_kwargs):
        info(f"Configuring: {self.config}")
        self._config = Config(
            alt_name=self.config["AltName"],
            include_assets=self.config["IncludeAssets"],
            asset_dir=self.config["AssetDir"],
            patch_style=self.config["PatchStyle"],
            site_url=config.get("site_url", "/"),
            site_dir=config["site_dir"],
            temp_dir=TemporaryDirectory(),
        )
        return config

    def on_page_content(self, html, page, config, files, **_kwargs):
        soup = BeautifulSoup(html, "html.parser")

        for img_tag in soup.find_all("img", {"src": re.compile(r"\.svg$")}):
            if self._config.alt_name != WILDCARD and img_tag["alt"] != self._config.alt_name:
                continue
            debug(f'inlining {img_tag} -> {img_tag["src"]}')

            svg_data = get_svg_data(img_tag["src"], files, self._config)
            if svg_data:
                svg_tag = get_svg_tag(svg_data, self._config)
                if self._config.include_assets:
                    svg_tag = include_assets(svg_tag, files, self._config)
                img_tag.replace_with(svg_tag)

        return str(soup)
