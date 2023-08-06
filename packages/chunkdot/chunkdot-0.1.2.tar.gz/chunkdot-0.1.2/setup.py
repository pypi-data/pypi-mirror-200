# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chunkdot']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.56.4,<0.57.0', 'numpy>=1.23,<2.0', 'scipy>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'chunkdot',
    'version': '0.1.2',
    'description': 'Multi-threaded matrix multiplication and cosine similarity calculations.',
    'long_description': "# ChunkDot\n\nMulti-threaded matrix multiplication and cosine similarity calculations. Appropriate for the calculation of the K most similar items for a large number of items (~1 Million) by partitioning the item matrix representation (embeddings) and using Numba to accelerate the calculations.\n\n## Usage\n\n```bash\npip install -U chunkdot\n```\n\nCalculate the 50 most similar and dissimilar items for 100K items.\n\n```python\nimport numpy as np\nfrom chunkdot import cosine_similarity_top_k\n\nembeddings = np.random.randn(100000, 256)\n# using all you system's memory\ncosine_similarity_top_k(embeddings, top_k=50)\n# most dissimilar items using 20GB\ncosine_similarity_top_k(embeddings, top_k=-50, max_memory=20E9)\n```\n```\n<100000x100000 sparse matrix of type '<class 'numpy.float64'>'\n with 5000000 stored elements in Compressed Sparse Row format>\n```\n\n## The execution time\n\n```python\nfrom timeit import timeit\nimport numpy as np\nfrom chunkdot import cosine_similarity_top_k\n\nembeddings = np.random.randn(100000, 256)\ntimeit(lambda: cosine_similarity_top_k(embeddings, top_k=50, max_memory=20E9), number=1)\n```\n```\n58.611996899999994\n```\n",
    'author': 'Rodrigo Agundez',
    'author_email': 'rragundez@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
