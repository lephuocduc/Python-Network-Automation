from CheckIPInterface import *
from unittest.mock import mock_open
import pytest

def test_case01():
    assert 'python'.upper()=='PYTHON'

def get_user_input():
    return input("Enter your name: ")

def test_get_user_input(monkeypatch):
    user_input = "John Doe"
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    assert get_user_input() == user_input
    
def test_get_credentials(monkeypatch):
    user_input = "username"
    password_input = "password"
    monkeypatch.setattr("builtins.input", lambda prompt: user_input)
    monkeypatch.setattr("getpass.getpass", lambda prompt: password_input)
    assert get_credentials() == (user_input,password_input)

def test_get_interfaces_from_file(monkeypatch, tmp_path):
    mock_file_path = tmp_path / "filepath.txt"
    mock_file_content = "interface1\ninterface2\ninterface3"
    monkeypatch.setattr("builtins.input", lambda prompt: mock_file_path)
    monkeypatch.setattr("builtins.open", mock_open(read_data = mock_file_content))
    assert get_interfaces_from_file() == ["interface1","interface2","interface3"]

def test_get_interfaces_from_file_file_error(monkeypatch, tmp_path):
    with pytest.raises(FileNotFoundError):
        mock_file_path = tmp_path / "filepath.txt"
        monkeypatch.setattr("builtins.input", lambda prompt: mock_file_path)
        get_interfaces_from_file()