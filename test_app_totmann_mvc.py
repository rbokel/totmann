import unittest
import app_totmann_mvc as app


class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = app.Model()
        self.model.on_change_state = self.mock_on_change_state
        self.model.on_change_countdown = self.mock_on_change_countdown
        self.state_changed = False
        self.countdown_changed = False

    def mock_on_change_state(self):
        self.state_changed = True

    def mock_on_change_countdown(self):
        self.countdown_changed = True

    def test_update_time_waiting_for_timeout(self):
        self.model.state = app.Model.STATE_WAITING_FOR_TIMEOUT
        self.model.countdown = 1
        self.model.update_time()
        self.assertEqual(self.model.countdown, self.model.countdown_length)
        self.assertTrue(self.countdown_changed)
        self.assertTrue(self.state_changed)
        self.assertEqual(self.model.state, app.Model.STATE_COUNTING_DOWN)

    def test_update_time_counting_down(self):
        self.model.state = app.Model.STATE_COUNTING_DOWN
        self.model.countdown = 1
        self.model.update_time()
        self.assertEqual(self.model.countdown, self.model.alarm_length)
        self.assertTrue(self.countdown_changed)
        self.assertTrue(self.state_changed)
        self.assertEqual(self.model.state, app.Model.STATE_ALARMING)

    def test_update_time_init(self):
        self.model.state = app.Model.STATE_INIT
        self.model.countdown = 1
        self.model.update_time()
        self.assertEqual(self.model.countdown, self.model.timeout_length)
        self.assertTrue(self.countdown_changed)
        self.assertTrue(self.state_changed)
        self.assertEqual(self.model.state, app.Model.STATE_WAITING_FOR_TIMEOUT)

    def test_update_time_no_timeout(self):
        self.model.state = app.Model.STATE_WAITING_FOR_TIMEOUT
        self.model.countdown = 10
        self.model.update_time()
        self.assertEqual(self.model.countdown, 9)
        self.assertTrue(self.countdown_changed)
        self.assertFalse(self.state_changed)


if __name__ == "__main__":
    unittest.main()
