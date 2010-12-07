
import unittest

from trackers.hammy import HamsterTracker
from hamster import client

class HammyTest(unittest.TestCase):

    def setUp(self):
        self.tracker = HamsterTracker()

    def test_create_100_activites(self):
        tags = []
        ids = []
        try:
            for i in range(1,100):
                ids.append(self.tracker.start("activity-%d" % i,
                                              "",
                                              "some elaborate desciption",
                                              tags))
        finally:
            # clean up!
            for id in ids:
                self.tracker.storage.remove_fact(id)
