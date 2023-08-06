# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cenfind',
 'cenfind.cli',
 'cenfind.core',
 'cenfind.experiments',
 'cenfind.labelbox',
 'cenfind.publication']

package_data = \
{'': ['*']}

install_requires = \
['albumentations>=1.3.0,<2.0.0',
 'csbdeep>=0.7.3,<0.8.0',
 'labelbox>=3.36.1,<4.0.0',
 'llvmlite==0.39.1',
 'numba==0.56.4',
 'numpy>=1.23.5,<2.0.0',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'ortools==9.4.1874',
 'pandas>=1.4.1,<2.0.0',
 'protobuf==3.19.6',
 'python-dotenv>=0.21.1,<0.22.0',
 'pytomlpp>=1.0.10,<2.0.0',
 'scikit-image>=0.19.2,<0.20.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'scipy>=1.7.1,<2.0.0',
 'spotipy-detector>=0.1.0,<0.2.0',
 'stardist>=0.8.3,<0.9.0',
 'tifffile>=2022.5.4,<2023.0.0',
 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{':sys_platform == "arm64"': ['tensorflow-macos==2.9.0'],
 ':sys_platform == "win32" or sys_platform == "linux"': ['tensorflow>=2.9.0,<3.0.0']}

entry_points = \
{'console_scripts': ['cenfind = cenfind.__main__:main',
                     'evaluate = cenfind.cli.evaluate:main',
                     'upload = cenfind.labelbox.upload_labels:main',
                     'vignettes = cenfind.labelbox.vignettes:main']}

setup_kwargs = {
    'name': 'cenfind',
    'version': '0.11.6',
    'description': 'Score cells for centrioles in IF data',
    'long_description': "# CenFind\n\nA command line interface to score cells for centrioles.\n\n## Introduction\n\n`cenfind` is a command line interface to detect and assign centrioles in immunofluorescence images of human cells. Specifically, it orchestrates:\n\n- the z-max projection of the raw files;\n- the detection of centrioles;\n- the detection of the nuclei;\n- the assignment of the centrioles to the nearest nucleus.\n\n## Installation\n1. Install python via pyenv\n2. Download and set up 3.9.5 as local version\n3. Set up Python interpreter\n```shell\npyenv local 3.9.5\npyenv global 3.9.5\n```\n4. Create a virtual environment for CenFind\n```shell\npython -m venv venv-cenfind\nsource venv-cenfind/bin/activate\n```\n\n5. Check that `cenfind`'s programs are correctly installed by running:\n\n```shell\ncenfind squash --help\n```\n\n## Basic usage\nBefore scoring the cells, you need to prepare the dataset folder. \n`cenfind` assumes a fixed folder structure. \nIn the following we will assume that the .ome.tif files are all immediately in raw/. \nEach file is a z-stack field of view (referred to as field, in the following) containing 4 channels (0, 1, 2, 3). The channel 0 contains the nuclei and the channels 1-3 contains centriolar markers.\n\n```text\n<project_name>/\n└── raw/\n```\n2. Run `prepare` to initialise the dataset folder with a list of output folders:\n```shell\ncenfind prepare /path/to/dataset --splits 1 2 --projection_suffix _max\n```\n```shell\nusage: CENFIND prepare [-h] [--projection_suffix PROJECTION_SUFFIX] [--splits SPLITS [SPLITS ...]] dataset\n\npositional arguments:\n  dataset               Path to the dataset\n\noptions:\n  -h, --help            show this help message and exit\n  --projection_suffix PROJECTION_SUFFIX\n                        Suffix indicating projection, e.g., `_max` or `Projected`, empty if not specified (default: )\n  --splits SPLITS [SPLITS ...]\n                        Write the train and test splits for continuous learning using the channels specified (default: None)\n```\n\n2. Run `squash` with the path to the project folder and the suffix of the raw files. `projections/` is populated with the max-projections `*_max.tif` files.\n```shell\ncenfind squash path/to/dataset\n```\n```shell\nusage: CENFIND squash [-h] dataset\n\npositional arguments:\n  dataset     Path to the dataset folder\n\noptions:\n  -h, --help  show this help message and exit\n\n```\n\n3. Run `score` with the arguments source, the index of the nuclei channel (usually 0 or 3), the channel to score and the path to the model. You need to download it from https://figshare.com/articles/software/Cenfind_model_weights/21724421\n```shell\ncenfind score /path/to/dataset /path/to/model/ -n 0 -c 1 2 3 -v 50\n```\n```shell\nusage: CENFIND score [-h] --channel_nuclei CHANNEL_NUCLEI --channel_centrioles CHANNEL_CENTRIOLES [CHANNEL_CENTRIOLES ...] [--vicinity VICINITY] [--factor FACTOR] [--cpu]\n                     dataset model\n\npositional arguments:\n  dataset               Path to the dataset\n  model                 Absolute path to the model folder\n\noptions:\n  -h, --help            show this help message and exit\n  --channel_nuclei CHANNEL_NUCLEI, -n CHANNEL_NUCLEI\n                        Channel index for nuclei segmentation, e.g., 0 or 3 (default: None)\n  --channel_centrioles CHANNEL_CENTRIOLES [CHANNEL_CENTRIOLES ...], -c CHANNEL_CENTRIOLES [CHANNEL_CENTRIOLES ...]\n                        Channel indices to analyse, e.g., 1 2 3 (default: None)\n  --vicinity VICINITY, -v VICINITY\n                        Distance threshold in pixel (default: 50 px) (default: 50)\n  --factor FACTOR       Factor to use: given a 2048x2048 image, 256 if 63x; 2048 if 20x: (default: 256)\n  --cpu                 Only use the cpu (default: False)\n```\n\n4. Check that the predictions are satisfactory by looking at the folders `visualisations/` and `statistics/`\n\n5. If you are interested in categorising the number of centrioles, run `cenfind analyse path/to/dataset --by <well>` the --by option is interesting if you want to group your scoring by well, if the file names obey to the rule `<WELLID_FOVID>`.\n\n```shell\nusage: CENFIND analyse [-h] --by BY dataset\n\npositional arguments:\n  dataset     Path to the dataset\n\noptions:\n  -h, --help  show this help message and exit\n  --by BY     Grouping (field or well) (default: None)\n```\n\n## Running `cenfind score` in the background\n\nWhen you exit the shell, running programs receive the SIGHUP, which aborts them. This is undesirable if you need to close your shell for some reasons. Fortunately, you can make your program ignore this signal by prepending the program with the `nohup` command. Moreover, if you want to run your program in the background, you can append the ampersand `&`. In practice, run `nohup cenfind score ... &` instead of `cenfind score ...`.\n\nThe output will be written to the file `nohup.out` and you can peek the progress by running `tail -F nohup.out`, the flag `-F` will refresh the screen as the file is being written. Enter Ctrl-C to exit the tail program.\n\nIf you want to kill the program score, run  `jobs` and then run `kill <jobid>`. If you see no jobs, check the log `nohup.out`; it can be done or the program may have crashed, and you can check the error there.\n\n## Evaluating the quality of the model on a new dataset\n\nThe initial model M is fitted using a set of five representative datasets, hereafter referred to as the standard datasets (DS1-5). \nIf your type of data deviates too much from the standard dataset, M may perform less well. \n\nSpecifically, when setting out to score a new dataset, you may be faced with one of three situations, as reflected by the corresponding F1 score (i.e., 2TP/2TP+FN+FP, TP: true positive, FP: false positive; FN: false negative): \n(1) the initial model (M) performs well on the new dataset (0.9 ≤ F1 ≤ 1); in this case, model M is used; \n(2) model M performs significantly worse on the new dataset (0.5 ≤ F1 < 0.9); in this case, you may want to consider retraining the model (see below); \n(3) the model does not work at all (0 ≤  F1 < 0.5); such a low F1value probably means that the features of the data set are too distant from the original representative data set to warrant retraining starting from M. \n\nBefore retraining a model (2), verify once more the quality of the data, which needs to be sufficiently good in terms of signal over noise to enable efficient learning. \nIf this is not the case, it is evident that the model will not be able to learn well. \nIf you, as a human being, cannot tell the difference between a real focus and a stray spot using a single channel at hand (i.e., not looking at other channels), the same will hold for the model. \n\nTo retrain the model, you first must annotate the dataset, divide it randomly into training and test sets (90 % versus 10 % of the data, respectively). \nNext, the model is trained with the 90 % set, thus generating a new model, M*. \nLast, you will evaluate the gain of performance on the new dataset, as well as the potential loss of performance on the standard datasets. \n\n### Detailed training procedure:\n1.\tSplit the dataset into training (90%) and test (10%) sets, each containing one field of view and the channel to use. This helps trace back issues during the training and renders the model fitting reproducible.\n```shell\n```\n2.\tLabel all the images present in training and test sets using Labelbox. To upload the images, please create the vignettes first and then upload them once you have a project set up.\n```shell\ncenfind vignettes /path/to/dataset\ncenfind upload /path/to/dataset --env /path/to/.env\n```\n3.\tSave all foci coordinates (x, y), origin at top-left, present in one field of view as one text file under /path/to/dataset/annotation/centrioles/ with the naming scheme <dataset_name>_max_C<channel_index>.txt.\n```shell\ncenfind download dataset-name --env /path/to/.env\n```\n4.\tEvaluate the newly annotated dataset using the model M by computing the F1 score.\nevaluate dataset model\n\n```shell\nusage: CENFIND evaluate [-h] [--performances_file PERFORMANCES_FILE] [--tolerance TOLERANCE] --channel_nuclei CHANNEL_NUCLEI --channel_centrioles CHANNEL_CENTRIOLES [CHANNEL_CENTRIOLES ...]\n                        [--vicinity VICINITY]\n                        dataset model\n\npositional arguments:\n  dataset               Path to the dataset folder\n  model                 Path to the model\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --performances_file PERFORMANCES_FILE\n                        Path of the performance file, STDOUT if not specified (default: None)\n  --tolerance TOLERANCE\n                        Distance in pixels below which two points are deemed matching (default: 3)\n  --channel_nuclei CHANNEL_NUCLEI\n                        Channel index for nuclei segmentation, e.g., 0 or 3 (default: None)\n  --channel_centrioles CHANNEL_CENTRIOLES [CHANNEL_CENTRIOLES ...]\n                        Channel indices to analyse, e.g., 1 2 3 (default: None)\n  --vicinity VICINITY   Distance threshold in micrometer (default: -5 um) (default: -5)\n```\n5.\tIf the performance is poor (i.e., F1 score < 0.9), fit a new model instance, M*, with the standard dataset plus the new dataset (90% in each case).\n6.\tTest performance of model M* on the new data set; hopefully the F1 score will now be ≥ 0.9 (if not: consider increasing size of annotated data).\n7.\tTest performance of model M* on the standard datasets; if performance of F1* ≥ F1, then save M* as the new M (otherwise keep M* as a separate model for the new type of data set).\n\n\n## Internal API\n\n`cenfind` consists of two core classes: `Dataset` and `Field`.\n\nsetup function that \n- write the toml file\n- write the field.txt that list all the files\n- create the folders projections, predictions, visualisations and statistics\n\nA `Dataset` represents a collection of related fields and should:\n- construct file names for fields\n- split the fileds into train, test and validate\n- load all fields or only for a specific split\n\nA `Field` represents a field of view and should:\n- get Dataset\n- load the projection as np.ndarray\n- load the channel as np.ndarray\n- detect centrioles => list of Points\n- detect nuclei => list of Contours\nif present:\n- load annotation as np.ndarray\n- load mask as np.ndarray\n\nA scoring function that \n- assigns centrioles to nuclei (contours, points) => pairs\n- compares predictions with annotation (points, points) => metrics_namespace\n\nVisualisation functions that:\n- outline centrioles and nuclei (data, points) => image\n- create composite vignettes (data) => composite_image\n- flag partial nuclei (contours, tolerance) => contours\n",
    'author': 'Leo Burgy',
    'author_email': 'leo.burgy@epfl.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/UPGON/cenfind',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
