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


class TestContainerNodes(unittest.TestCase):
    """Test API generation with nested and non-nested container nodes."""
    @classmethod
    def setUpClass(cls):
        cls.testdir = os.path.join(os.path.dirname(__file__), 'data')
        cls.openapi_dir = os.path.join(cls.testdir, 'openapi')
        cls.user = 'testrest'
        cls.proxyhost = 'localhost:8480'
        cls.devicename = 'CSR1K-7'

        set_base_path(cls.testdir)
        cls.ys = YSYangSet.load(cls.user, 'testcontainer')
        # set up for testing nested container(s)
        cls.ctx_nested = YSContext(
            cls.ys, modulenames=['test-nested-container']
        )
        cls.ym_nested = YSYangModels(cls.ctx_nested, ['test-nested-container'])
        cls.psy_nested = cls.ym_nested.yangs['test-nested-container']
        # set up for testing non-nested container(s)
        cls.ctx = YSContext(cls.ys, modulenames=['test-container'])
        cls.ym = YSYangModels(cls.ctx, ['test-container'])
        cls.psy = cls.ym.yangs['test-container']

    def setUp(self):
        """Function called before starting test execution."""
        self.tmpdir = tempfile.mkdtemp()
        self.maxDiff = None

    def tearDown(self):
        """Remove the test directory."""
        shutil.rmtree(self.tmpdir)

    def test_nested_container(self):
        """Generate APIs for a nested container with 4 levels."""
        node_ids = ['/top-level-container']
        modulename = 'test-nested-container'
        depth_limit = None
        host = YSDeviceProfile.get(self.devicename)
        ParseRestconf(
            self.user, modulename, self.ctx_nested, node_ids, host,
            depth_limit, proxyhost=self.proxyhost
        )

        if ParseRestconf.cached_head and ParseRestconf.cached_paths:
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

    def test_container(self):
        """Generate APIs for a container with 1 level."""
        node_ids = ['/top-level-container']
        modulename = 'test-container'
        depth_limit = None
        host = YSDeviceProfile.get(self.devicename)
        ParseRestconf(
            self.user, modulename, self.ctx, node_ids, host,
            depth_limit, proxyhost=self.proxyhost
        )

        if ParseRestconf.cached_head and ParseRestconf.cached_paths:
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
