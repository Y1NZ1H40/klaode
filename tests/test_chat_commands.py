from pathlib import Path

from klaode.app import KlaodeApp
from klaode.ui.chat_screen import ChatScreen
from klaode.ui.welcome_screen import WelcomeScreen

TEXTS_DIR = Path(__file__).resolve().parent.parent / "texts"
SNIPPETS_DIR = Path(__file__).resolve().parent.parent / "snippets"


async def _log_in(pilot) -> None:
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause(0.9)


async def _type(pilot, text: str) -> None:
    for char in text:
        await pilot.press(char)
    await pilot.press("enter")
    await pilot.pause()


async def test_home_command_returns_to_login_screen() -> None:
    app = KlaodeApp(available_files=[TEXTS_DIR / "example.txt"], snippets_dir=SNIPPETS_DIR)
    async with app.run_test() as pilot:
        await _log_in(pilot)
        assert isinstance(app.screen, ChatScreen)

        await pilot.click("#chat-input")
        await _type(pilot, "home")

        assert isinstance(app.screen, WelcomeScreen)


async def test_quit_command_exits_app() -> None:
    app = KlaodeApp(available_files=[TEXTS_DIR / "example.txt"], snippets_dir=SNIPPETS_DIR)
    async with app.run_test() as pilot:
        await _log_in(pilot)

        await pilot.click("#chat-input")
        await _type(pilot, "quit")

        assert app._exit is True
