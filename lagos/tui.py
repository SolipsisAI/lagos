"""
From https://github.com/Textualize/textual/issues/157#issuecomment-965646368
"""
import string
from typing import Union

from rich.console import RenderableType
from textual import events
from textual.app import App
from textual.keys import Keys
from textual.reactive import Reactive
from textual.widget import Widget


class InputBox(Widget):
    input_text: Union[Reactive[str], str] = Reactive("")

    def render(self) -> RenderableType:
        return f"[blue]❯[/blue] {self.input_text}"

    def set_input_text(self, input_text: str) -> None:
        self.input_text = input_text


class MyApp(App):
    input_text: Union[Reactive[str], str] = Reactive("")

    input_box: InputBox

    async def on_key(self, key: events.Key) -> None:
        if key.key == Keys.ControlH:
            self.input_text = self.input_text[:-1]
        elif key.key == Keys.Delete:
            self.input_text = ""
        elif key.key in string.printable:
            self.input_text += key.key

    def watch_input_text(self, input_text) -> None:
        self.input_box.set_input_text(input_text)

    async def on_mount(self, event: events.Mount) -> None:
        self.input_box = InputBox()
        grid = await self.view.dock_grid(edge="left", name="left")
        grid.add_column(name="body")
        grid.add_row(size=1, name="input")
        grid.add_areas(areaInputBox="body,input")
        grid.place(areaInputBox=self.input_box)


MyApp.run(title="Message", log="textual.log")