> **NOTE:** this project is still WIP!

# mkdocs-inline-svg-plugin

[![PyPI - Version](https://img.shields.io/pypi/v/mkdocs-inline-svg-plugin.svg)](https://pypi.org/project/mkdocs-inline-svg-plugin)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-inline-svg-plugin.svg)](https://pypi.org/project/mkdocs-inline-svg-plugin)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install mkdocs-inline-svg-plugin
```

## License

`mkdocs-inline-svg-plugin` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Usage

If you want to inline SVGs, that were put in `img` tags by the [kroki plugin](https://github.com/AVATEAM-IT-SYSTEMHAUS/mkdocs-kroki-plugin):

`mkdocs.yml`:
```yaml
plugins:
  - kroki:
      FencePrefix: ''
      HttpMethod: 'POST'
      DownloadImages: true
  - inline-svg:
      AltName: Kroki
```

### Configuration

| Config value | What for |
|---|---|
| `AltName` | default: `*`, that does not check the `img` `alt` property |
| `IncludeAssets` | default: `False`, looks for `url(..)`, downloads the contents to `AssetDir` and replaces the url |
| `AssetDir` | default: `assets/` |
| `PatchStyle` | default: `False`, this feature is **EXPERIMENTAL** and not yet finished, needs an additional CSS |

## Test

Serve documentation:
```sh
hatch run docs:serve
```