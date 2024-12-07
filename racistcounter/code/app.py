from __future__ import annotations
from pathlib import Path
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Label, Button
from textual_fspicker import FileOpen, Filters
from textual_imageview.viewer import ImageViewer
from PIL import Image
import os

class RacistCounter(App):
    """RACISTCOUNTER - Checks Black and White Pixels in a Bitmap Image (BMP or PNG)"""

    CSS_PATH = "app.tcss"


    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Label("  _____            _     _    _____                  _            \n |  __ \          (_)   | |  / ____|                | |           \n | |__) |__ _  ___ _ ___| |_| |     ___  _   _ _ __ | |_ ___ _ __ \n |  _  // _` |/ __| / __| __| |    / _ \| | | | '_ \| __/ _ \ '__|\n | | \ \ (_| | (__| \__ \ |_| |___| (_) | |_| | | | | ||  __/ |   \n |_|  \_\__,_|\___|_|___/\__|\_____\___/ \__,_|_| |_|\__\___|_|   \n                                                                  \nUpload An Image to Start:")
        yield Button("Choose an Image", id="chooseFile")
        yield Label("No Output Yet...", id="output")
        yield ImageViewer(Image.open("icon.png")) 
        yield Label("\nRacistCounter v1.1 - Part of the RandomApps Collection\nMade by SebAndBlocks 2024 ©️TurquoiseTNT Multimedia https://github.com/sebandblocks/randomapps/racistcounter", id="cp")

    def show_selected(self, to_show: Path | None) -> None:
        self.query_one("#output", Label).update("Working...")
        if to_show is None:
            self.query_one("#output", Label).update("Cancelled.")
            return
        else:
            if not os.path.exists(str(to_show)):
                self.query_one("#output", Label).update("Couldn't find that file...")
                return
            try:
                with Image.open(str(to_show)) as img:
                    #img = img.convert("1")
                    pixels = list(img.getdata())
                    black_count = pixels.count(0)
                    white_count = pixels.count(255)
                    self.query_one(ImageViewer).remove()
                    new_viewer = ImageViewer(img)
                    self.mount(new_viewer, before=self.query_one("#cp"))
                    self.query_one("#output", Label).update(f"Black: {black_count}\nWhite: {white_count}")
                    return black_count, white_count
            except Exception as e:
                self.query_one("#output", Label).update("Couldn't load image... Weird.")

    @on(Button.Pressed, "#chooseFile")
    def open_file(self) -> None:
        """Show the `FileOpen` dialog when the button is pushed."""
        self.push_screen(
            FileOpen(
                ".",
                filters=Filters(
                    (".PNG", lambda p: p.suffix.lower() == ".png"),
                    (".BMP", lambda p: p.suffix.lower() in (".bmp")),
                ),
            ),
            callback=self.show_selected,
        )
if __name__ == "__main__":
    app = RacistCounter()
    app.run()