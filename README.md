# Class for autotests GoogleAppEngine python apps
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/test.helper.gae/test.helper.gae%20tests?label=Python%202.7&style=plastic)](https://github.com/vb64/test.helper.gae/actions?query=workflow%3A%22test.helper.gae+tests%22)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/17fdd38a1f2f487bb1d50124f6f99b93)](https://www.codacy.com/manual/vb64/test.helper.gae?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vb64/test.helper.gae&amp;utm_campaign=Badge_Grade)

## Install
```bash
$ pip install tester-gae
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
        self.queue = Queue('default')
        self.queue.add(Task('xxx', url='/'))

        self.assert_tasks_num(1)
        tasks = self.gae_tasks(queue_name='default', flush_queue=False)

        self.assertEqual(len(tasks), 1)
        self.assert_tasks_num(1)

        tasks = self.gae_tasks(queue_name='default', flush_queue=True)
        self.assertEqual(len(tasks), 1)
        self.assert_tasks_num(0)

```
