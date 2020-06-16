# Class for autotests GoogleAppEngine Standard Environment Python2.7 apps
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/test.helper.gae/test.helper.gae%20tests?label=Python%202.7&style=plastic)](https://github.com/vb64/test.helper.gae/actions?query=workflow%3A%22test.helper.gae+tests%22)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/17fdd38a1f2f487bb1d50124f6f99b93)](https://www.codacy.com/manual/vb64/test.helper.gae?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vb64/test.helper.gae&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/17fdd38a1f2f487bb1d50124f6f99b93)](https://www.codacy.com/manual/vb64/test.helper.gae?utm_source=github.com&utm_medium=referral&utm_content=vb64/test.helper.gae&utm_campaign=Badge_Coverage)

## Install
```bash
pip install tester-gae
```

## Usage in tests

```python

from google.appengine.ext import ndb
from google.appengine.api.taskqueue import Queue, Task

from tester_gae import TestGae


class TestTable(ndb.Model):
    """
    GAE datatsore table
    """
    date = ndb.DateTimeProperty(auto_now_add=True)


class TestGaeApp(TestGae):
    """
    test GAE app
    """
    def setUp(self):
        TestGae.setUp(self, "path/to/you/gae/app/dir")  # where app.yaml located
        self.queue = Queue('default')
        self.queue.add(Task('xxx', url='/'))

    def test_check_db_tables(self):
        """
        check db table items count
        """
        self.check_db_tables([
          (TestTable, 0),
        ])

        item = TestTable()
        item.put()

        self.check_db_tables([
          (TestTable, 1),
        ])

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

    def test_flask_execute(self):
        """
        execute queue in fask app context
        """
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
```
