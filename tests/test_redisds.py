from dragline import redisds
import unittest
import pickle


class RedisQueueTest(unittest.TestCase):

    def setUp(self):
        self.queue = redisds.Queue("test")
        self.queue.clear()

    def tearDown(self):
        self.queue.clear()

    def test_push(self):
        self.queue.put("test string")
        self.assertFalse(self.queue.empty())

    def test_pop(self):
        self.queue.put("second test string")
        self.assertFalse(self.queue.empty())
        self.assertEqual("second test string", self.queue.get())
        self.assertTrue(self.queue.empty())

    def test_serialization(self):
        self.queue.serializer = pickle
        test_data = {'id': 1234, 'name': "ashwin"}
        self.queue.put(test_data)
        self.assertEqual(self.queue.get(), test_data)

    def test_get_nowait(self):
        value = self.queue.get_nowait()
        self.assertEqual(value, None)


class RedisSetTest(unittest.TestCase):

    def setUp(self):
        self.set = redisds.Set("test")
        self.set.clear()

    def tearDown(self):
        self.set.clear()

    def test_add(self):
        self.assertTrue(self.set.empty())
        self.set.add("test string")
        self.assertFalse(self.set.empty())
        self.assertTrue("test string" in self.set)

    def test_remove(self):
        self.set.add("second test string")
        self.assertFalse(self.set.empty())
        self.set.remove("second test string")
        self.assertFalse("second test string" in self.set)
        self.assertTrue(self.set.empty())


class RedisCounterTest(unittest.TestCase):

    def setUp(self):
        self.count = redisds.Counter("test", value=0)

    def test_inc(self):
        self.assertEqual(self.count.get(), 0)
        self.count.inc()
        self.assertEqual(self.count.get(), 1)

    def test_decr(self):
        self.assertEqual(self.count.get(), 0)
        self.count.decr()
        self.assertEqual(self.count.get(), -1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
