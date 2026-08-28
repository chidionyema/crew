"""R49-no-secrets-in-chat — founder 2026-08-28: "we dont send password here".

A Sunshine password was sent to the home channel by a session (deleted, rotated). pr-evidence now refuses
a PR body carrying `<secret word>=<value>`; an env NAME or a path after the word is a pointer and passes.
"""
import importlib.util
from importlib.machinery import SourceFileLoader
from pathlib import Path

PE = Path(__file__).resolve().parents[1] / "scripts" / "pr-evidence.py"
loader = SourceFileLoader("pr_evidence_r49", str(PE))
spec = importlib.util.spec_from_file_location("pr_evidence_r49", PE, loader=loader)
pe = importlib.util.module_from_spec(spec)
loader.exec_module(pe)


def test_value_after_a_secret_word_is_a_leak():
    assert pe.secret_in("creds set: user founder password=" + "hunter" + "2222wxyz" + " done") is not None
    assert pe.secret_in("TOKEN: 'ghp_abcdefghijklmnop'") is not None


def test_env_name_or_path_is_a_pointer_not_a_leak():
    assert pe.secret_in("token=TELEGRAM_BOT_TOKEN read from the vault") is None
    assert pe.secret_in("password in ~/.estate/sunshine-founder.pass (0600)") is None
    assert pe.secret_in("api_key: OPENROUTER_API_KEY") is None
