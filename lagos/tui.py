# app.py
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Dict, List

from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text
from textual import events
from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Footer, Header, ScrollView

from textual_inputs import TextInput

from lagos.bot import Bot, BotEvent

if TYPE_CHECKING:
    from textual.message import Message


class CustomHeader(Header):
    """Override the default Header for Styling"""

    def __init__(self) -> None:
        super().__init__()
        self.tall = False
        self.style = Style(color="white", bgcolor="rgb(98,98,98)")

    def render(self) -> Table:
        header_table = Table.grid(padding=(0, 1), expand=True)
        header_table.add_column(justify="left", ratio=0, width=8)
        header_table.add_column("title", justify="center", ratio=1)
        header_table.add_column("clock", justify="right", width=8)
        header_table.add_row(
            "", self.full_title, self.get_clock() if self.clock else ""
        )
        return header_table

    async def on_click(self, event: events.Click) -> None:
        return await super().on_click(event)


class CustomFooter(Footer):
    """Override the default Footer for Styling"""

    def make_key_text(self) -> Text:
        """Create text containing all the keys."""
        text = Text(
            style="white on rgb(98,98,98)",
            no_wrap=True,
            overflow="ellipsis",
            justify="left",
            end="",
        )
        for binding in self.app.bindings.shown_keys:
            key_display = (
                binding.key.upper()
                if binding.key_display is None
                else binding.key_display
            )
            hovered = self.highlight_key == binding.key
            key_text = Text.assemble(
                (f" {key_display} ", "reverse" if hovered else "default on default"),
                f" {binding.description} ",
                meta={"@click": f"app.press('{binding.key}')", "key": binding.key},
            )
            text.append_text(key_text)
        return text


class MessageList(Widget):
    """Override the default Header for Styling"""

    mouse_over = Reactive(False)

    def __init__(self, messages: List[Dict] = None) -> None:
        super().__init__()
        self.tall = True
        if messages is None:
            messages = []
        self.messages = messages
        self.table = None
        self.scroll_view = None

    def on_mount(self):
        self.table = Table.grid(padding=(0, 1), expand=True)
        self.table.add_column(
            "timestamp", justify="left", ratio=0, width=7, style="magenta"
        )
        self.table.add_column(
            "username", justify="right", ratio=0, width=15, style="green"
        )
        self.table.add_column("text", justify="left", ratio=1)
        self.update_messages()
        self.set_interval(0.1, self.update_messages)

    def update_messages(self):
        if not self.messages:
            return

        message = self.messages.pop(0)
        timestamp = message.timestamp
        username = message.username
        text = message.text
        self.table.add_row(timestamp, f"{username} [blue]|[/blue] ", text)
        self.refresh()

    def render(self) -> Table:
        return self.table


class Chat(App):

    current_index: Reactive[int] = Reactive(-1)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bot = None
        self.tab_index = ["message_input"]

    async def on_load(self) -> None:
        await self.bind("q", "quit", "Quit")
        await self.bind("enter", "submit", "Submit")
        await self.bind("escape", "reset_focus", show=False)
        await self.bind("ctrl+i", "next_tab_index", show=False)
        await self.bind("shift+tab", "previous_tab_index", show=False)

    async def on_mount(self) -> None:
        self.header = CustomHeader()
        await self.view.dock(self.header, edge="top")
        await self.view.dock(CustomFooter(), edge="bottom")

        self.message_list = MessageList()

        self.message_input = TextInput(
            name="message_input",
            placeholder="Enter your message",
            title="",
        )
        self.message_input.on_change_handler_name = "handle_message_input_on_change"

        # Setup Grid
        grid = await self.view.dock_grid()

        grid.add_column(name="col")

        grid.add_row(name="top", fraction=5)
        grid.add_row(name="bottom", fraction=1, size=3)

        grid.add_areas(
            message_list="col-start|col-end,top",
            message_input="col-start|col-end,bottom",
        )

        grid.set_align("stretch", "stretch")

        grid.place(
            message_list=self.message_list,
            message_input=self.message_input,
        )

        self.bot = Bot()

    async def action_next_tab_index(self) -> None:
        """Changes the focus to the next form field"""
        if self.current_index < len(self.tab_index) - 1:
            self.current_index += 1
            await getattr(self, self.tab_index[self.current_index]).focus()

    async def action_previous_tab_index(self) -> None:
        """Changes the focus to the previous form field"""
        if self.current_index > 0:
            self.current_index -= 1
            await getattr(self, self.tab_index[self.current_index]).focus()

    async def action_submit(self) -> None:
        text = self.message_input.value

        bot_event = BotEvent(username="bitjockey", text=text)
        self.bot.receive(bot_event)

        self.message_list.messages.append(bot_event)
        self.message_input.value = ""

    async def action_reset_focus(self) -> None:
        self.current_index = -1
        await self.header.focus()

    async def handle_message_input_on_change(self, message: Message) -> None:
        self.log(f"Message input change: {message.sender.value}")
