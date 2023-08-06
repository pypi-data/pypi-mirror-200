

<img src="docsource/_static/nsaphx_logo.png" alt="Logo" height="50">


[![codecov](https://codecov.io/gh/NSAPH-Software/nsaphx/branch/develop/graph/badge.svg?token=8aSueNmHZN)](https://codecov.io/gh/NSAPH-Software/nsaphx)

nsaphx is a Python package designed for causal inference studies under the potential outcome framework. It provides a flexible and extensible framework for defining and applying computational instructions to input data, which should include outcome, exposure, and confounders. The package uses a directed acyclic graph and database storage to ensure efficient computation and storage of each object. Instruction handlers can be easily extended by defining new classes and methods, which can then be used to create new instructions that can be applied to data. Each object is computed only once and stored in the database, ensuring that computation is efficient and data is not duplicated.

## Installation

### PyPI

```bash
pip install nsaphx
```

### Source

Please note that the package requires Python 3.7 or higher.

```bash
git clone https://github.com/NSAPH-Software/nsaphx
cd nsaphx
pip install .
```

