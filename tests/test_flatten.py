import pytest
from unittest.mock import patch, MagicMock
from src.flatten import flatten
from src.Config import Config

@pytest.fixture
def mock_dependencies():
    with patch("src.flatten.DF") as mock_df, \
         patch("src.flatten.UI") as mock_ui, \
         patch("src.flatten.Logger") as mock_logger, \
         patch("src.flatten.Config") as mock_config:
        mock_df.get_files_in_directory.return_value = []
        mock_ui.progress.add_task.return_value = "main_task"
        mock_config.TLDN = "test_directory"
        yield mock_df, mock_ui, mock_logger, mock_config

# Parametrized test cases for happy path, edge cases, and error cases
@pytest.mark.parametrize("test_id, files_in_directory, expected_files_after_move, expected_log_messages", [
    ("happy_path", ["file1.txt", "file2.txt"], ["file1.txt", "file2.txt"], ["[green]Flattening complete!", "[cyan]Files after move: 2", "[cyan]Files found: 2", "[green]All files moved successfully!"]),
    ("empty_directory", [], [], None),
    ("nonexistent_directory", None, None, None),
])
def test_flatten(mock_dependencies, test_id, files_in_directory, expected_files_after_move, expected_log_messages):
    mock_df, mock_ui, mock_logger, mock_config = mock_dependencies

    # Arrange
    mock_df.get_files_in_directory.side_effect = [files_in_directory, expected_files_after_move]  # First call for before, second for after
    if files_in_directory is not None:
        mock_df.process_file = MagicMock()

    # Act
    flatten()

    # Assert
    if files_in_directory is not None and files_in_directory:
        mock_df.process_file.assert_called()
        mock_ui.progress.update.assert_called_with("main_task", advance=1)
        assert mock_df.cleanup.call_count == 1
    if expected_log_messages:
        for log_message in expected_log_messages:
            mock_logger.write.assert_any_call(log_message)
    else:
        mock_logger.write.assert_not_called()