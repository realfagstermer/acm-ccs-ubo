# encoding=utf8
from doit import get_var

import os
import logging
import logging.config

logging.config.fileConfig('logging.cfg', )
logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('rdflib').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

import data_ub_tasks

config = {
    'dumps_dir': get_var('dumps_dir', '/opt/data.ub/www/default/dumps'),
    'dumps_dir_url': get_var('dumps_dir_url', 'http://data.ub.uio.no/dumps'),
    'graph': 'http://data.ub.uio.no/acm-ccs-ubo',
    'fuseki': 'http://localhost:3031/ds',
    'basename': 'acm-ccs-ubo',
    'git_user': 'ubo-bot',
    'git_email': 'danmichaelo+ubobot@gmail.com',
}


def task_txt2ttl():
    return {
        'doc': 'Convert txt files to ttl',
        'actions': [
            'mkdir -p dist',
            'python txt2ttl.py src/ids.yml src/ccs1998.txt dist/ccs1998.ttl',
            'python txt2ttl.py src/ids.yml src/cybernetics.txt dist/cybernetics.ttl',
        ],
        'file_dep': [
            'src/ccs1998.txt',
            'src/cybernetics.txt',
        ],
        'targets': [
            'dist/ccs1998.ttl',
            'dist/cybernetics.ttl',
        ]
    }


def task_build():
    return {
        'doc': 'Run skosify',
        'actions': [
            'mkdir -p dist',
            'skosify -c skosify.cfg -F turtle src/acm-ccs-ubo.scheme.ttl dist/ccs1998.ttl dist/cybernetics.ttl -o dist/%(basename)s.ttl' % config,
            'skosify -c skosify.cfg -F nt dist/%(basename)s.ttl -o dist/%(basename)s.nt' % config,
            'skosify -c skosify.cfg -F xml dist/%(basename)s.ttl -o dist/%(basename)s.rdf.xml' % config,
        ],
        'file_dep': [
            'dist/ccs1998.ttl',
            'dist/cybernetics.ttl',
        ],
        'targets': [
            'dist/%(basename)s.ttl' % config,
            'dist/%(basename)s.nt' % config,
            'dist/%(basename)s.rdf.xml' % config,
        ]
    }


def task_publish_dumps():
    return data_ub_tasks.publish_dumps_task_gen(config['dumps_dir'], [
        '%s.rdf.xml' % config['basename'],
        '%s.ttl' % config['basename'],
        '%s.nt' % config['basename'],
        # '%s.mappings.nt' % config['basename'],
    ])


def task_fuseki():
    return data_ub_tasks.fuseki_task_gen(config, [
        'dist/%(basename)s.ttl' % config,
        # 'dist/%(basename)s.mappings.nt' % config,
    ])
