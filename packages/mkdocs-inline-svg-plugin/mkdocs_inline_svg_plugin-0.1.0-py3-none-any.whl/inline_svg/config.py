from dataclasses import dataclass
from tempfile import TemporaryDirectory


@dataclass
class Config:
    alt_name: str
    include_assets: bool
    asset_dir: str
    patch_style: bool
    site_url: str
    site_dir: str
    temp_dir: TemporaryDirectory
