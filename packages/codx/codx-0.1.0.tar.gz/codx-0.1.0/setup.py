# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codx']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.81,<2.0', 'pandas>=1.5.3,<2.0.0', 'uniprotparser>=1.0.9,<2.0.0']

setup_kwargs = {
    'name': 'codx',
    'version': '0.1.0',
    'description': 'A package used to retrieve exon for protein sequences from RefSeqGene database',
    'long_description': '# CODX\n--\n\ncodx is a python package that allow retrieval of exons data from NCBI RefSeqGene database.\n\n## Installation\n\n```bash\npip install codx\n```\n\n## Usage\n\n```python\n# Import the create_db function to create a sqlite3 database with gene and exon data from NCBI\nfrom codx.components import create_db\n\n\n# 120892 is the gene id for LRRK2 gene\ndb = create_db(["120892"])\n\n# From the database object, you can retrieve a gene object using its gene name\ngene = db.get_gene("LRRK2")\n\n# From the gene objects you can retrieve exons data from the blocks attribute each exon object has its start and end location as well as the associated sequence\nfor exon in gene.blocks:\n    print(exon.start, exon.end, exon.sequence)\n\n# Using the gene object it is also possible to create all possible ordered combinations of exons\n# This will be a generator object that yield a SeqRecord object for each combination\n# There however may be a lot of combinations so depending on the gene, you may not want to use this with a very large gene unless there are no other options\nfor exon_combination in gene.shuffle_blocks():\n    print(exon_combination)\n\n# To create six frame translation of any sequence, you can use the three_frame_translation function twice, one with and one without the reverse complement option enable\n# Each output is a dictionary with the translatable sequence as value and the frame as key\nfrom codx.components import three_frame_translation\nfor exon_combination in gene.shuffle_blocks():\n    three_frame = three_frame_translation(exon_combination.seq, only_start_at_atg=True)\n    three_frame_complement = three_frame_translation(exon_combination.seq, only_start_at_atg=True, reverse_complement=True)\n\n```\n',
    'author': 'Toan Phung',
    'author_email': 'toan.phungkhoiquoctoan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
