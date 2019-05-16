"""
make test T=test_tester_gae
"""
import os
from tester_gae import TestGae

PROJECT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gae')


class TestSetup(TestGae):
    """
    Test SetUp method
    """
    def setUp(self):
        pass

    def test_default(self):
        """
        GAE services enabled
        """
        TestGae.setUp(self, PROJECT_DIR)

        from main import TestTable
        item = TestTable()
        item.put()
        self.assertTrue(item)

    def test_args(self):
        """
        GAE services disabled
        """
        TestGae.setUp(
          self,
          PROJECT_DIR,
          datastore=False,
          memcache=False,
          app_identity=False,
          blobstore=False,
          files=False,
          images=False,
          taskqueue=False,
          urlfetch=False,
          mail=False,
          user=False,
          capability=False,
          channel=False,
          logservice=False,
          xmpp=False,
          search=False
        )

        from main import TestTable
        item = TestTable()

        with self.assertRaises(AssertionError):
            item.put()


class TestDatastore(TestGae):
    """
    Test testbed datastore_v3_stub
    """
    def setUp(self):
        TestGae.setUp(self, PROJECT_DIR)

        from main import TestTable
        self.item = TestTable()
        self.item.put()

    def test_reread(self):
        """
        bypass memcash read
        """
        item1 = self.reread(self.item.key)
        self.assertEqual(self.item.key, item1.key)

    def test_check_db_tables(self):
        """
        check db table items count
        """
        from main import TestTable
        self.check_db_tables([
          (TestTable, 1),
        ])


class TestTaskQueue(TestGae):
    """
    Test testbed task queue
    """
    def setUp(self):
        TestGae.setUp(self, PROJECT_DIR)
        from google.appengine.api.taskqueue import Queue, Task

        self.queue = Queue('default')
        self.queue.add(Task('xxx', url='/'))

    def test_queue(self):
        """
        check for number of tasks in queue
        """
        self.assert_tasks_num(1)
        tasks = self.gae_tasks(queue_name='default', flush_queue=False)

        self.assertEqual(len(tasks), 1)
        self.assert_tasks_num(1)

        tasks = self.gae_tasks(queue_name='default', flush_queue=True)
        self.assertEqual(len(tasks), 1)
        self.assert_tasks_num(0)