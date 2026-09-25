import asyncio
from pathlib import Path

from klaode.app import KlaodeApp
from klaode.ui.chat_screen import ChatScreen
from klaode.ui.welcome_screen import BONUS_ROAST_METHOD, LOGIN_METHODS, ROAST_MESSAGE, WelcomeScreen

SNIPPETS_DIR = Path(__file__).resolve().parent.parent / "snippets"


async def test_login_options_show_one_per_available_file(tmp_path) -> None:
    file_a = tmp_path / "a.txt"
    file_a.write_text("Content A")
    file_b = tmp_path / "b.txt"
    file_b.write_text("Content B")

    app = KlaodeApp(available_files=[file_a, file_b], snippets_dir=SNIPPETS_DIR)
    async with app.run_test() as pilot:
        await pilot.pause()
        rendered = str(app.screen.query_one("#login-options").render())

        assert "a.txt" in rendered
        assert "b.txt" in rendered
        assert "3." not in rendered


async def test_selecting_a_login_method_opens_its_matching_file(tmp_path) -> None:
    file_a = tmp_path / "a.txt"
    file_a.write_text("Content A")
    file_b = tmp_path / "b.txt"
    file_b.write_text("Content B")

    app = KlaodeApp(available_files=[file_a, file_b], snippets_dir=SNIPPETS_DIR)
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.press("down")
        await pilot.press("enter")
        await asyncio.sleep(1.5)
        await pilot.pause()

        assert isinstance(app.screen, ChatScreen)
        assert app.screen._text_path == file_b


async def test_login_options_are_capped_at_ten_with_bonus_roast_option(tmp_path) -> None:
    files = []
    for i in range(12):
        file_path = tmp_path / f"file{i:02d}.txt"
        file_path.write_text(f"Content {i}")
        files.append(file_path)

    app = KlaodeApp(available_files=files, snippets_dir=SNIPPETS_DIR)
    async with app.run_test() as pilot:
        await pilot.pause()
        rendered = str(app.screen.query_one("#login-options").render())

        for method in LOGIN_METHODS:
            assert method in rendered
        assert "file10.txt" not in rendered
        assert "file11.txt" not in rendered
        assert BONUS_ROAST_METHOD in rendered
        assert "11." in rendered


async def test_no_bonus_roast_option_with_ten_or_fewer_files(tmp_path) -> None:
    files = []
    for i in range(10):
        file_path = tmp_path / f"file{i:02d}.txt"
        file_path.write_text(f"Content {i}")
        files.append(file_path)

    app = KlaodeApp(available_files=files, snippets_dir=SNIPPETS_DIR)
    async with app.run_test() as pilot:
        await pilot.pause()
        rendered = str(app.screen.query_one("#login-options").render())

        assert BONUS_ROAST_METHOD not in rendered


async def test_selecting_bonus_roast_option_stays_on_welcome_screen(tmp_path) -> None:
    files = []
    for i in range(12):
        file_path = tmp_path / f"file{i:02d}.txt"
        file_path.write_text(f"Content {i}")
        files.append(file_path)

    app = KlaodeApp(available_files=files, snippets_dir=SNIPPETS_DIR)
    async with app.run_test() as pilot:
        await pilot.pause()
        for _ in range(10):
            await pilot.press("down")

        # pilot.press awaits the full action, including the roast flow's
        # own sleeps, so by the time it returns the roast has already
        # played out and reset itself; the observable outcome is that we
        # never left the welcome screen and it is ready to accept input again.
        await pilot.press("enter")
        await pilot.pause()

        assert isinstance(app.screen, WelcomeScreen)
        assert app.screen._logging_in is False


async def test_bonus_roast_message_is_shown_mid_flight(tmp_path) -> None:
    files = []
    for i in range(12):
        file_path = tmp_path / f"file{i:02d}.txt"
        file_path.write_text(f"Content {i}")
        files.append(file_path)

    app = KlaodeApp(available_files=files, snippets_dir=SNIPPETS_DIR)
    async with app.run_test() as pilot:
        await pilot.pause()
        for _ in range(10):
            await pilot.press("down")

        select_task = asyncio.ensure_future(app.screen.action_select())
        await asyncio.sleep(0.9)
        status = str(app.screen.query_one("#login-status").render())
        assert ROAST_MESSAGE in status

        await select_task
