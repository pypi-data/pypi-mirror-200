# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perceiver',
 'perceiver.data',
 'perceiver.data.text',
 'perceiver.data.vision',
 'perceiver.model',
 'perceiver.model.core',
 'perceiver.model.text',
 'perceiver.model.vision',
 'perceiver.scripts',
 'perceiver.scripts.text',
 'perceiver.scripts.vision']

package_data = \
{'': ['*']}

install_requires = \
['cchardet>=2.1,<3.0',
 'einops>=0.4,<0.5',
 'fairscale>=0.4,<0.5',
 'fsspec[s3]',
 'jsonargparse[signatures]>=4.12,<5.0',
 'pytorch-lightning>=1.7,<2.0',
 'tensorboard>=2.11,<3.0',
 'torch-optimizer>=0.3,<0.4',
 'torch>=1.13,<2.0',
 'torchmetrics>=0.9,<0.10']

extras_require = \
{'text': ['datasets>=2.4,<3.0',
          'tokenizers>=0.12,<0.13',
          'transformers>=4.21,<5.0'],
 'vision': ['datasets>=2.4,<3.0',
            'torchvision>=0.14,<0.15',
            'opencv-python>=4.6.0.66,<5.0.0.0']}

setup_kwargs = {
    'name': 'perceiver-io',
    'version': '0.8.2',
    'description': 'Perceiver IO',
    'long_description': '# Perceiver, Perceiver IO and Perceiver AR\n\nThis repository is a PyTorch and PyTorch Lightning implementation of\n\n<table>\n  <tr>\n    <td>\n       <b>Perceiver</b>: General Perception with Iterative Attention\n       (<a href="https://arxiv.org/abs/2103.03206">paper</a>,\n        <a href="https://www.youtube.com/watch?v=P_xeshTnPZg">video</a>)\n    </td>\n    <td><img src="docs/images/small-perceiver.png" alt="Perceiver"/></td>\n  </tr>\n  <tr>\n    <td>\n      <b>Perceiver IO</b>: A General Architecture for Structured Inputs & Outputs\n      (<a href="https://arxiv.org/abs/2107.14795">paper</a>,\n       <a href="https://www.deepmind.com/blog/building-architectures-that-can-handle-the-worlds-data">blog post</a>)\n    </td>\n    <td><img src="docs/images/small-perceiver-io.png" alt="Perceiver IO"/></td>\n  </tr>\n  <tr>\n    <td>\n      General-purpose, long-context autoregressive modeling with <b>Perceiver AR</b>\n      (<a href="https://arxiv.org/abs/2202.07765">paper</a>,\n       <a href="https://www.deepmind.com/blog/perceiver-ar-general-purpose-long-context-autoregressive-generation">blog post</a>)\n    </td>\n    <td><img src="docs/images/small-perceiver-ar.png" alt="Perceiver AR"/></td>\n  </tr>\n</table>\n\nAll model classes are written in plain PyTorch and can be wrapped into [PyTorch Lightning](https://pytorch-lightning.readthedocs.io/en/stable/)\nmodules for training at scale. The command line interface is implemented with the [Lightning CLI](https://pytorch-lightning.readthedocs.io/en/stable/cli/lightning_cli.html).\n[Pretrained weights](docs/pretrained-models.md) can be imported for [official models](docs/pretrained-models.md#official-models)\nfrom the 🤗 Hub, [training checkpoints](docs/pretrained-models.md#training-checkpoints) from [training examples](docs/training-examples.md)\nare available for download too. Datasets used in the training examples are 🤗 [datasets](https://huggingface.co/docs/datasets)\nwrapped into PyTorch Lightning [data modules](perceiver/data). For NLP tasks, this library supports all 🤗\n[fast tokenizers](https://huggingface.co/docs/transformers/fast_tokenizers) and the 🤗 Perceiver UTF-8 bytes tokenizer.\n\n## Installation\n\n### Via pip\n\n```shell\npip install perceiver-io[text,vision]\n```\n\n### From sources\n\nInstallation from sources requires a [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and a\n[Poetry](https://python-poetry.org/docs/#installation) (1.2.0 or higher) installation.\n\nCreate and activate the `perceiver-io` conda environment:\n\n```shell\nconda env create -f environment.yml\nconda activate perceiver-io\n```\n\nInstall main and test dependencies, including all extras:\n\n```shell\n# Without dependencies required for examples\npoetry install --all-extras\n```\n\nIf you want to run the [examples](examples) locally, additionally use `--with examples`:\n\n```shell\npoetry install --all-extras --with examples\n```\n\n### Docker image\n\n```shell\ndocker pull ghcr.io/krasserm/perceiver-io:latest\n```\n\nSee [Docker image](docs/docker-image.md) for details.\n\n## Documentation\n\n- [Getting started](docs/getting-started.md)\n- [Model construction](docs/model-construction.md)\n- [Pretrained models](docs/pretrained-models.md)\n- [Training examples](docs/training-examples.md)\n- [Inference examples](examples/inference.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krasserm/perceiver-io/blob/0.8.1/examples/inference.ipynb)\n- [Building blocks](docs/building-blocks.md)\n\n## Articles\n\nArticles referencing this repository:\n\n- [Training compute-optimal Perceiver AR language models](https://krasserm.github.io/2023/01/23/scaling-perceiver-ar/)\n- [A gentle introduction to Rotary Position Embedding](https://krasserm.github.io/2022/12/13/rotary-position-embedding/)\n\n## Other implementations\n\n- [Perceiver](https://paperswithcode.com/paper/perceiver-general-perception-with-iterative#code)\n- [Perceiver IO](https://paperswithcode.com/paper/perceiver-io-a-general-architecture-for#code)\n- [Perceiver AR](https://paperswithcode.com/paper/general-purpose-long-context-autoregressive#code)\n',
    'author': 'Martin Krasser',
    'author_email': 'krasserm@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/krasserm/perceiver-io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
