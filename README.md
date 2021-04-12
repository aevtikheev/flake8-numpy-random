# flake8-numpy-random
Plugin for Flake8 that forbids usage of numpy.random()

## Installation
```bash
pip install flake8-numpy-random
```
## Motivation
Using NumPy’s random number generator with multi-process data loading in PyTorch causes identical augmentations unless you specifically set seeds using the worker_init_fn option in the DataLoader. Details - https://tanelp.github.io/posts/a-bug-that-plagues-thousands-of-open-source-ml-projects/

## Error codes
| Error code |       Description         |
|:----------:|:-------------------------:|
|    NPR001  | do not use numpy.random() |

## License
MIT
