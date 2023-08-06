# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tablelinker',
 'tablelinker.convertors.basics',
 'tablelinker.convertors.extras',
 'tablelinker.core']

package_data = \
{'': ['*']}

install_requires = \
['charset-normalizer>=3.0.1,<4.0.0',
 'docopt>=0.6.2,<0.7.0',
 'fugashi>=1.2.1,<2.0.0',
 'install>=1.3.5,<2.0.0',
 'ipadic>=1.0.0,<2.0.0',
 'jaconv>=0.3.3,<0.4.0',
 'jageocoder>=1.4.0,<2.0.0',
 'jeraconv>=0.2.1,<0.3.0',
 'munkres>=1.1.4,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'torch>=1.13.1,<2.0.0',
 'transformers>=4.25.1,<5.0.0',
 'xlrd>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['tablelinker = tablelinker.cli:main']}

setup_kwargs = {
    'name': 'tablelinker-lib',
    'version': '1.0.0',
    'description': 'A library of processes for manipulating tabular data in CSV format',
    'long_description': '# tablelinker-lib\n\nTableLinker をコマンドライン / プログラム組み込みで利用するためのライブラリ。\n\n## インストール手順\n\nPoetry を利用します。\n\n```\n$ poetry install --with group=dev\n$ poetry shell\n```\n\nMacOS の場合、デフォルトの python バージョンが 3.11 なので\npytorch がインストールできません。以下の手順が必要です。\n\n```\n% pyenv install 3.10\n% poetry env use 3.10\n% poetry shell\n% poetry install --with group=dev\n```\n\n## コマンドラインで利用する場合\n\ntablelinker モジュールを実行すると、標準入力から受け取った CSV を\nコンバータで変換し、標準出力に送るパイプとして利用できます。\n\n```\n$ cat sample/datafiles/yanai_tourism.csv | \\\n  python -m tablelinker sample/taskfiles/task.json\n```\n\n利用するコンバータと、コンバータに渡すパラメータは JSON ファイルに記述し、\nパラメータで指定します。\n\n## 組み込んで利用する場合\n\n`sample.py` を参照してください。\n',
    'author': 'Akiko Aizawa',
    'author_email': 'akiko@nii.ac.jp',
    'maintainer': 'Takeshi Sagara',
    'maintainer_email': 'sagara@info-proto.com',
    'url': 'https://github.com/KMCS-NII/tablelinker-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11.0',
}


setup(**setup_kwargs)
