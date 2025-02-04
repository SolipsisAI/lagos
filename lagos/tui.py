# app.py
from __future__ import annotations

from typing import TYPE_CHECKING, List

from rich.style import Style
from rich.table import Table
from rich.text import Text
from textual import events
from textual.app import App
from textual.widget import Widget, Reactive
from textual.widgets import Footer, Header, ScrollView

from textual_inputs import TextInput

if TYPE_CHECKING:
    from textual.message import Message

from lagos.bot import Bot
from lagos.records import MessageRecord


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
    """List view for messages"""

    def __init__(self, messages: List[MessageRecord] = None) -> None:
        super().__init__()
        self._table = None
        self.tall = True
        self.messages = messages if bool(messages) else []

    def update_messages(self):
        for message in self.messages:
            self._table.add_row(
                message.timestamp, f"{message.username} [blue]|[/blue] ", message.text
            )

    def render(self) -> Table:
        self._table = Table.grid(padding=(0, 1), expand=True)
        self._table.add_column(
            "timestamp", justify="left", ratio=0, width=20, style="magenta"
        )
        self._table.add_column(
            "username", justify="right", ratio=0, width=20, style="green"
        )
        self._table.add_column("text", justify="left", ratio=1)
        self.update_messages()

        return self._table


class Chat(App):

    current_index: Reactive[int] = Reactive(-1)
    last_message_id: Reactive[int] = Reactive(0)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tab_index: List[str] = ["message_input"]

    def add_message(self, message: MessageRecord):
        self.message_list.messages.append(message)
        self.last_message_id = self.message_list.messages[-1].id

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
        self.message_view = ScrollView(gutter=1)
        self.message_input = TextInput(
            name="message_input",
            placeholder="Enter your message",
            title="",
        )
        self.message_input.on_change_handler_name = "handle_message_input_on_change"

        grid = await self.view.dock_grid()

        grid.add_column(name="col")

        grid.add_row(name="top", fraction=5)
        grid.add_row(name="bottom", fraction=1, size=3)

        grid.add_areas(
            message_view="col-start|col-end,top",
            message_input="col-start|col-end,bottom",
        )

        grid.set_align("stretch", "stretch")

        grid.place(
            message_view=self.message_view,
            message_input=self.message_input,
        )

        self.bot = Bot(daemon=True, callback=self.add_message)

    async def watch_last_message_id(self, value: int) -> None:
        self.message_list.refresh()
        await self.message_view.update(self.message_list)
        self.message_view.page_down()

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
        self.message_input.value = ""

        if not text:
            return

        message = MessageRecord(
            {
                "username": "bitjockey",
                "author_id": 2,
                "text": text,
            }
        )

        await self.bot.add(message)

    async def action_reset_focus(self) -> None:
        self.current_index = -1
        await self.header.focus()

    async def handle_message_input_on_change(self, message: Message) -> None:
        self.log(f"Message input change: {message.sender.value}")


if __name__ == "__main__":
    Chat.run(title="Solipsis", log="textual.log")
