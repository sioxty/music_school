import unittest

from tests.fixtures import create_test_engine, create_test_session, populate_sample_school


class TestFixtures(unittest.TestCase):
    def test_create_test_engine_and_session(self):
        engine = create_test_engine()
        session = create_test_session(engine)
        self.assertIsNotNone(session)
        session.close()

    def test_populate_sample_school(self):
        session = create_test_session()
        data = populate_sample_school(session)

        self.assertIn("teacher", data)
        self.assertIn("subject", data)
        self.assertIn("group", data)
        self.assertIn("student", data)
        self.assertIn("lesson", data)
        self.assertIn("grade", data)

        self.assertEqual(data["teacher"].name, "Olena")
        self.assertEqual(data["subject"].name, "Piano")
        self.assertEqual(data["group"].name, "Junior Ensemble")
        self.assertEqual(data["student"].name, "Alice")
        self.assertEqual(data["grade"].value, 11)

        session.close()


if __name__ == "__main__":
    unittest.main()
