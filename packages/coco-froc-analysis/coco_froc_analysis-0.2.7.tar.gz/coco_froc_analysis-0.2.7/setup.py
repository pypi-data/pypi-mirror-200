# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coco_froc_analysis', 'coco_froc_analysis.count', 'coco_froc_analysis.froc']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.5,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'coco-froc-analysis',
    'version': '0.2.7',
    'description': 'FROC analysis for COCO detections for Detectron(2) and OpenMMLab',
    'long_description': '# COCO FROC analysis\n\nFROC analysis for COCO annotations and Detectron(2) detection results. The COCO annotation style is defined [here](https://cocodataset.org/).\n\n### Installation\n\n```bash\npip install coco-froc-analysis\n```\n\n### About\n\nA single annotation record in the ground-truth file might look like this:\n\n```json\n{\n  "area": 2120,\n  "iscrowd": 0,\n  "bbox": [111, 24, 53, 40],\n  "category_id": 3,\n  "ignore": 0,\n  "segmentation": [],\n  "image_id": 407,\n  "id": 945\n}\n```\n\nWhile the prediction (here for bounding box) given by the region detection framework is such:\n\n```json\n{\n  "image_id": 407,\n  "category_id": 3,\n  "score": 0.9990422129631042,\n  "bbox": [\n    110.72555541992188,\n    13.9161834716797,\n    49.4566650390625,\n    36.65155029296875\n  ]\n}\n```\n\nThe FROC analysis counts the number of images, number of lesions in the ground truth file for all categories and then counts the lesion localization predictions and the non-lesion localization predictions. A lesion is localized by default if its center is inside any ground truth box and the categories match or if you wish to use IoU you should provide threshold upon which you can define the \'close enough\' relation.\n\n## Usage\n\n```python\nfrom coco_froc_analysis.count import generate_bootstrap_count_curves\nfrom coco_froc_analysis.count import generate_count_curve\nfrom coco_froc_analysis.froc import generate_bootstrap_froc_curves\nfrom coco_froc_analysis.froc import generate_froc_curve\n\n# For single FROC curve\ngenerate_froc_curve(\n            gt_ann=args.gt_ann,\n            pr_ann=args.pr_ann,\n            use_iou=args.use_iou,\n            iou_thres=args.iou_thres,\n            n_sample_points=args.n_sample_points,\n            plot_title=\'FROC\' if args.plot_title is None else args.plot_title,\n            plot_output_path=\'froc.png\' if args.plot_output_path is None else args.plot_output_path,\n            test_ann=args.test_ann,\n        )\n\n# For bootstrapped curves\ngenerate_bootstrap_froc_curves(\n            gt_ann=args.gt_ann,\n            pr_ann=args.pr_ann,\n            n_bootstrap_samples=args.bootstrap,\n            use_iou=args.use_iou,\n            iou_thres=args.iou_thres,\n            n_sample_points=args.n_sample_points,\n            plot_title=\'FROC (bootstrap)\' if args.plot_title is None else args.plot_title,\n            plot_output_path=\'froc_bootstrap.png\' if args.plot_output_path is None else args.plot_output_path,\n            test_ann=args.test_ann,\n        )\n```\n\nPlease check `run.py` for more details. The `IoU` part of this code is not reliable and currently the codebase only works for binary evaluation, but any multiclass problem could be chunked up to work with it.\n\nDescription of `run.py` arguments:\n\n```bash\nusage: run.py [-h] [--bootstrap BOOTSTRAP] --gt_ann GT_ANN --pr_ann PR_ANN [--use_iou] [--iou_thres IOU_THRES] [--n_sample_points N_SAMPLE_POINTS]\n              [--plot_title PLOT_TITLE] [--plot_output_path PLOT_OUTPUT_PATH] [--test_ann TEST_ANN] [--counts] [--weighted]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --bootstrap BOOTSTRAP\n                        Whether to do a single or bootstrap runs.\n  --gt_ann GT_ANN\n  --pr_ann PR_ANN\n  --use_iou             Use IoU score to decide based on `proximity`\n  --iou_thres IOU_THRES\n                        If IoU score is used the default threshold is set to .5\n  --n_sample_points N_SAMPLE_POINTS\n                        Number of points to evaluate the FROC curve at.\n  --plot_title PLOT_TITLE\n  --plot_output_path PLOT_OUTPUT_PATH\n  --test_ann TEST_ANN   Extra ground-truth like annotations\n  --counts\n  --weighted\n```\n\n## CLI Usage\n\n```bash\npython -m coco_froc_analysis [-h] [--bootstrap N_BOOTSTRAP_ROUNDS] --gt_ann GT_ANN --pred_ann PRED_ANN [--use_iou] [--iou_thres IOU_THRES] [--n_sample_points N_SAMPLE_POINTS]\n                        [--plot_title PLOT_TITLE] [--plot_output_path PLOT_OUTPUT_PATH]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --bootstrap  N_ROUNDS Whether to do a single or bootstrap runs.\n  --gt_ann GT_ANN\n  --pred_ann PRED_ANN\n  --use_iou             Use IoU score to decide on `proximity` rather then using center pixel inside GT box.\n  --iou_thres IOU_THRES\n                        If IoU score is used the default threshold is arbitrarily set to .5\n  --n_sample_points N_SAMPLE_POINTS\n                        Number of points to evaluate the FROC curve at.\n  --plot_title PLOT_TITLE\n  --plot_output_path PLOT_OUTPUT_PATH\n```\n\nBy default centroid closeness is used, if the `--use_iou` flag is set, `--iou_thres` defaults to `.75` while the `--score_thres` score defaults to `.5`. The code outputs the FROC curve on the given detection results and GT dataset.\n\n## For developers\n\n### Running tests\n\n```bash\npython -m coverage run -m unittest discover --pattern "*_test.py" -v\npython -m coverage report -m\n```\n\n### Building and publishing (reminder)\n\n```bash\nact # for local CI pipeline\npdoc -d google coco_froc_analysis -o docs # build docs\npoetry version prerelease/patch # test or actual release\npoetry publish --build -r test-pypi # or without -r test-pypi for publishing to pypi\n```\n\n@Regards, Alex\n\n```\n@misc{qbeer,\n  author       = {Alex Olar},\n  title        = {FROC analysis for COCO-like file format},\n  howpublished = {GitHub repository},\n  month        = {September},\n  year         = {2022},\n  url          = {https://github.com/qbeer/coco-froc-analysis}\n}\n```\n',
    'author': 'Alex Olar',
    'author_email': 'olaralex666@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
