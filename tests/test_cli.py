import unittest
from unittest.mock import patch

from click.testing import CliRunner

import main


class CliSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    @patch("main.init_db")
    def test_main_help_shows_command_groups(self, init_db_mock):
        result = self.runner.invoke(main.cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("student", result.output)
        self.assertIn("teacher", result.output)
        self.assertIn("subject", result.output)
        self.assertIn("group", result.output)
        self.assertIn("lesson", result.output)
        self.assertIn("grade", result.output)
        self.assertIn("report", result.output)
        self.assertFalse(init_db_mock.called)

    @patch("main.init_db")
    def test_student_group_help(self, init_db_mock):
        result = self.runner.invoke(main.cli, ["student", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("add", result.output)
        self.assertIn("list", result.output)
        self.assertIn("show", result.output)
        self.assertIn("delete", result.output)

    @patch("main.init_db")
    def test_teacher_group_help(self, init_db_mock):
        result = self.runner.invoke(main.cli, ["teacher", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("add", result.output)
        self.assertIn("list", result.output)
        self.assertIn("show", result.output)
        self.assertIn("delete", result.output)

    @patch("main.init_db")
    def test_subject_group_help(self, init_db_mock):
        result = self.runner.invoke(main.cli, ["subject", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("add", result.output)
        self.assertIn("list", result.output)
        self.assertIn("delete", result.output)

    @patch("main.init_db")
    def test_group_group_help(self, init_db_mock):
        result = self.runner.invoke(main.cli, ["group", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("add", result.output)
        self.assertIn("list", result.output)
        self.assertIn("show", result.output)
        self.assertIn("add-student", result.output)
        self.assertIn("remove-student", result.output)
        self.assertIn("delete", result.output)

    @patch("main.init_db")
    def test_lesson_group_help(self, init_db_mock):
        result = self.runner.invoke(main.cli, ["lesson", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("add", result.output)
        self.assertIn("list", result.output)
        self.assertIn("delete", result.output)

    @patch("main.init_db")
    def test_grade_group_help(self, init_db_mock):
        result = self.runner.invoke(main.cli, ["grade", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("add", result.output)
        self.assertIn("list-student", result.output)
        self.assertIn("list-lesson", result.output)
        self.assertIn("delete", result.output)

    @patch("main.init_db")
    def test_report_group_help(self, init_db_mock):
        result = self.runner.invoke(main.cli, ["report", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("student", result.output)
        self.assertIn("group", result.output)
        self.assertIn("summary", result.output)


if __name__ == "__main__":
    unittest.main()
