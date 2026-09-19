"""Regression checks for catalog policy and evidence validation."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('catalog', Path(__file__).resolve().parents[1] / 'tools/check_catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


def fixture(host):
    plugins = [{'name': n, 'description': 'Test skill.', 'source': {'source': 'url', 'url': f'https://github.com/idnotbe/{n}.git'}} for n in catalog.NAMES]
    data = {'name': 'idnotbe', 'owner': {'name': 'idnotbe'}, 'description': 'Test catalog.', 'plugins': plugins}
    if host == 'codex':
        data.update(name='idnotbe-chatgpt-plugins', interface={'displayName': 'Test Catalog'})
        for plugin in plugins:
            plugin['policy'] = {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}
    return data


class CatalogTests(unittest.TestCase):
    def test_both_host_contracts(self):
        for host in ('claude', 'codex'):
            self.assertEqual(set(catalog.validate(fixture(host), host)), set(catalog.NAMES))

    def test_mutations_are_rejected(self):
        base = fixture('claude')
        mutations = [
            lambda x: x.update(name='wrong'),
            lambda x: x['plugins'].pop(),
            lambda x: x['plugins'].reverse(),
            lambda x: x['plugins'].append(copy.deepcopy(x['plugins'][-1])),
            lambda x: x['plugins'][0].update(source='./other'),
            lambda x: x['plugins'][0]['source'].update(sha='0' * 40),
            lambda x: x['plugins'][0]['source'].update(url='https://github.com/other/deep-inquiry.git'),
            lambda x: x['plugins'][0].update(skills='./unreviewed'),
            lambda x: x['plugins'][0].update(description=''),
        ]
        for mutation in mutations:
            data = copy.deepcopy(base)
            mutation(data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                catalog.validate(data, 'claude')

    def test_legacy_claude_entries_are_allowed(self):
        data = fixture('claude')
        data['plugins'].append({'name': 'other-plugin', 'description': 'Existing plugin.', 'source': {'source': 'url', 'url': 'https://github.com/idnotbe/other-plugin.git'}})
        data['plugins'].sort(key=lambda p: p['name'])
        self.assertEqual(set(catalog.validate(data, 'claude')), set(catalog.NAMES))

    def test_wrong_codex_policy_rejected(self):
        data = fixture('codex')
        data['plugins'][0]['policy']['installation'] = 'NOT_AVAILABLE'
        with self.assertRaises(ValueError):
            catalog.validate(data, 'codex')

    def test_discovery_uses_returned_path(self):
        response = {'marketplaces': [{'name': 'target', 'path': '/actual path', 'plugins': []}]}
        self.assertEqual(catalog.market_paths(response, 'target'), ['/actual path'])
        self.assertEqual(catalog.market_paths(response, 'unknown'), [])

    def test_missing_and_modified_bundle_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(ValueError):
                catalog.inventory(root)
            (root / 'SKILL.md').write_text('Original', encoding='utf-8')
            before = catalog.inventory(root)
            (root / 'SKILL.md').write_text('Changed', encoding='utf-8')
            self.assertNotEqual(before, catalog.inventory(root))


if __name__ == '__main__':
    unittest.main()
