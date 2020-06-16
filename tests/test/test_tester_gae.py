"""
make test T=test_tester_gae.py
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
        assert item

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

        with self.assertRaises(Exception) as context:
            self.reread(None)
        assert 'init_datastore_v3_stub not install' in str(context.exception)

        with self.assertRaises(Exception) as context:
            self.check_db_tables(None)
        assert 'init_datastore_v3_stub not install' in str(context.exception)

        with self.assertRaises(Exception) as context:
            self.gae_tasks()
        assert 'init_taskqueue_stub not install' in str(context.exception)


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
        assert self.item.key == item1.key

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

        assert len(tasks) == 1
        self.assert_tasks_num(1)

        tasks = self.gae_tasks(queue_name='default', flush_queue=True)
        assert len(tasks) == 1
        self.assert_tasks_num(0)

    def test_flask_execute(self):
        """
        execute queue in fask app context
        """
        from google.appengine.api.taskqueue import Task
        from flask import Flask
        app = Flask(__name__)
        app.config['TESTING'] = True

        @app.route('/', methods=['POST'])
        def root_page():
            """
            flask view
            """
            return 'OK'

        client = app.test_client()

        data = self.gae_tasks_dict()
        assert len(data) == 1
        task = data[data.keys()[0]]

        self.gae_task_flask_execute(task, client, is_delete=False, is_debug_print=True)
        data = self.gae_tasks_dict()
        assert len(data) == 1

        self.gae_task_flask_execute(task, client, is_debug_print=True)
        data = self.gae_tasks_dict()
        assert not data

        self.queue.add(Task('xxx', url='/'))

        self.gae_queue_flask_execute(client)
        data = self.gae_tasks_dict()
        assert not data

    def test_dict(self):
        """
        get queue content as dict
        """
        data = self.gae_tasks_dict()
        assert len(data) == 1
        assert 'task1' in data

    def test_dump(self):
        """
        dump queue content
        """
        self.gae_queue_dump()
        self.gae_queue_dump(fields=['name', 'url'])
