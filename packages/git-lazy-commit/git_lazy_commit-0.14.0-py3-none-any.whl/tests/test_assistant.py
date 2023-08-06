import unittest
from unittest.mock import MagicMock, patch, mock_open

from .context import assistant


class TestGitCommitAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = assistant.Assistant()

    def test_get_uncommitted_changes(self):
        with patch("subprocess.run") as run_mock:
            run_mock.return_value.stdout = "example change\n"
            changes = self.assistant.get_uncommitted_changes()
            self.assertEqual(changes, ["example change"])

    def test_generate_commit_message(self):
        changes_summary = "example change\n"
        with patch.object(
            self.assistant.chatgpt, "execute", return_value="Update example feature"
        ) as chatgpt_mock:
            commit_message = self.assistant.generate_commit_message(changes_summary)
            chatgpt_mock.assert_called_once()
            self.assertEqual(commit_message, "Update example feature")

    def test_commit_changes(self):
        repo_mock = MagicMock()
        commit_message = "Update example feature"
        self.assistant.commit_changes(repo_mock, commit_message)
        repo_mock.index.commit.assert_called_once_with(commit_message)

    def test_get_user_approval(self):
        commit_msg = "Update example feature"
        with patch("builtins.input", return_value="yes"):
            approval, message = self.assistant.get_user_approval(commit_msg)
            self.assertTrue(approval)
            self.assertEqual(message, commit_msg)

        with patch("builtins.input", return_value="no"):
            approval, message = self.assistant.get_user_approval(commit_msg)
            self.assertFalse(approval)
            self.assertEqual(message, commit_msg)

        with patch("builtins.input", side_effect=["invalid", "yes"]):
            approval, message = self.assistant.get_user_approval(commit_msg)
            self.assertTrue(approval)
            self.assertEqual(message, commit_msg)

        with patch.object(
            self.assistant,
            "edit_commit_message",
            return_value=(True, "Edited commit message"),
        ) as edit_mock:
            with patch("builtins.input", return_value="e"):
                approval, message = self.assistant.get_user_approval(
                    "Update example feature"
                )
                edit_mock.assert_called_once()
                self.assertTrue(approval)
                self.assertEqual(message, "Edited commit message")

    def test_generate_alternative_commit_message(self):
        with patch.object(
            self.assistant.chatgpt, "execute", return_value="Another commit message"
        ) as chatgpt_mock:
            alternative_commit_message = (
                self.assistant.generate_alternative_commit_message()
            )
            chatgpt_mock.assert_called_once()
            self.assertEqual(alternative_commit_message, "Another commit message")


if __name__ == "__main__":
    unittest.main()
