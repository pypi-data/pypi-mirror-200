import os
import unittest
import shutil
import tempfile
import json

from ysdevices import YSDeviceProfile
from ysfilemanager import YSYangSet
from ysyangtree import YSYangModels, YSContext
from yangsuite.paths import set_base_path
from ysrestconf import ParseRestconf
from ysrestconf.tests.util import compare_dicts


class TestListNodes(unittest.TestCase):
    """Test API generation with nested and non-nested container nodes."""
    @classmethod
    def setUpClass(cls):
        cls.testdir = os.path.join(os.path.dirname(__file__), 'data')
        cls.openapi_dir = os.path.join(cls.testdir, 'openapi')
        cls.user = 'testrest'
        cls.proxyhost = 'localhost:8480'
        cls.devicename = 'CSR1K-7'

        set_base_path(cls.testdir)
        cls.ys = YSYangSet.load(cls.user, 'testlist')
        # set up for testing nested list(s)
        cls.ctx_nested = YSContext(
            cls.ys, modulenames=['test-nested-list']
        )
        cls.ym_nested = YSYangModels(cls.ctx_nested, ['test-nested-list'])
        cls.psy_nested = cls.ym_nested.yangs['test-nested-list']
        # set up for testing non-nested list(s)
        cls.ctx = YSContext(cls.ys, modulenames=['test-list'])
        cls.ym = YSYangModels(cls.ctx, ['test-list'])
        cls.psy = cls.ym.yangs['test-list']

    def setUp(self):
        """Function called before starting test execution."""
        self.tmpdir = tempfile.mkdtemp()
        self.maxDiff = None

    def tearDown(self):
        """Remove the test directory."""
        shutil.rmtree(self.tmpdir)

    def test_nested_list(self):
        """Generate APIs for a nested list with 4 levels."""
        node_ids = ['/top-level-list']
        modulename = 'test-nested-list'
        depth_limit = None
        host = YSDeviceProfile.get(self.devicename)
        ParseRestconf(
            self.user, modulename, self.ctx_nested, node_ids, host,
            depth_limit, proxyhost=self.proxyhost
        )

        if ParseRestconf.cached_head and ParseRestconf.cached_head:
            # convert OpenAPI obj from OrderedDict to JSON
            openapi_actual = json.loads(
                json.dumps(
                    ParseRestconf.get_header(user=self.user, page=0)
                )
            )
            # get expected OpenAPI document
            with open(
                os.path.join(
                    self.openapi_dir, '{0}.json'.format(modulename)
                )
            ) as infile:
                openapi_expected = json.load(infile)
                compare_dicts(openapi_expected, openapi_actual)

    def test_list(self):
        """Generate APIs for a list with 1 level."""
        node_ids = ['/top-level-list']
        modulename = 'test-list'
        depth_limit = None
        host = YSDeviceProfile.get(self.devicename)
        ParseRestconf(
            self.user, modulename, self.ctx, node_ids, host,
            depth_limit, proxyhost=self.proxyhost
        )

        if ParseRestconf.cached_head and ParseRestconf.cached_head:
            # convert OpenAPI obj from OrderedDict to JSON
            openapi_actual = json.loads(
                json.dumps(
                    ParseRestconf.get_header(user=self.user, page=0)
                )
            )
            # get expected OpenAPI document
            with open(
                os.path.join(
                    self.openapi_dir, '{0}.json'.format(modulename)
                )
            ) as infile:
                openapi_expected = json.load(infile)
                compare_dicts(openapi_expected, openapi_actual)
