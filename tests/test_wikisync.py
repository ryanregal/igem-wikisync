from igem_wikisync.wikisync import run, get_upload_map, write_upload_map

import os
import yaml
import pytest


@pytest.fixture
def config():
    return {
        'src_dir': 'tests/data',
        'build_dir': 'tests/build',
        'team': 'BITSPilani-Goa_India'
    }


def test_get_upload_map_no_file():
    upload_map = get_upload_map()

    for key in ['html', 'css', 'js', 'assets']:
        assert key in upload_map.keys()
        assert isinstance(upload_map[key], dict)


def test_get_upload_map_empty_file():
    with open('upload_map.yml', 'w') as file:
        file.write('')

    upload_map = get_upload_map()

    for key in ['html', 'css', 'js', 'assets']:
        assert key in upload_map.keys()
        assert isinstance(upload_map[key], dict)

    if os.path.isfile('upload_map.yml'):
        os.remove('upload_map.yml')


def test_get_upload_map_semi_invalid_file():
    upload_map = {
        'html': None,
        'css': {}
    }

    with open('upload_map.yml', 'w') as file:
        yaml.safe_dump(upload_map, file)

    obtained_upload_map = get_upload_map()

    for key in ['html', 'css', 'js', 'assets']:
        assert key in obtained_upload_map.keys()
        assert isinstance(obtained_upload_map[key], dict)

    if os.path.isfile('upload_map.yml'):
        os.remove('upload_map.yml')


def test_get_upload_map_invalid_file():
    upload_map = {
        'html': [],
        'css': {}
    }

    with open('upload_map.yml', 'w') as file:
        yaml.safe_dump(upload_map, file)

    with pytest.raises(SystemExit):
        get_upload_map()

    if os.path.isfile('upload_map.yml'):
        os.remove('upload_map.yml')


def test_write_upload_map():
    upload_map = {
        'html': {
            'hello': {'link_URL': 'hello_link_URL'}
        },
        'css': {
            'hi': {'upload_URL': 'hi_upload_URL'}
        }
    }

    assert write_upload_map(upload_map)

    if os.path.isfile('upload_map.yml'):
        os.remove('upload_map.yml')


def test_run(config):

    run(config['team'], config['src_dir'], config['build_dir'])
