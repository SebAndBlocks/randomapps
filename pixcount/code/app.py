from __future__ import annotations
from pathlib import Path
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Label, Button
from textual.containers import Horizontal, Vertical
from textual_fspicker import FileOpen, Filters
from textual_imageview.viewer import ImageViewer
from PIL import Image
from matplotlib.colors import CSS4_COLORS
from scipy.spatial import KDTree
import os

def nearest_colour(rgb):
    color_names = list(CSS4_COLORS.keys())
    rgb_values = [tuple(int(CSS4_COLORS[name][1:][i:i+2], 16) for i in (0, 2, 4)) for name in color_names]
    tree = KDTree(rgb_values)
    _, idx = tree.query(rgb)
    return color_names[idx]

class PixCount(App):
    """PixCount - Checks Black and White Pixels in a Bitmap Image (BMP or PNG)"""

    CSS_PATH = "app.tcss"


    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Horizontal(
            Vertical(
                Label('____  __  _  _  ___  __   _  _  __ _  ____ \n(  _ \(  )( \/ )/ __)/  \ / )( \(  ( \(_  _)\n ) __/ )(  )  (( (__(  O )) \/ (/    /  )(  \n(__)  (__)(_/\_)\___)\__/ \____/\_)__) (__) \nUpload An Image to Start:'),
                Button("Choose an Image", id="chooseFile"),
                Label("No Output Yet...", id="output"),
                Label("\nPixCount™️ v1.2 - Part of the RandomApps Collection\nMade by SebAndBlocks")
            ),
            Vertical(
                ImageViewer(Image.open("icon.png")),
                Label("Image Viewer", id="cp")
            )
        )

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
                    img = img.convert("P", palette=Image.ADAPTIVE, colors=16)
                    color_counts = {}
                    palette = img.getpalette()
                    for count, color_index in img.getcolors():
                        r, g, b = palette[color_index * 3:color_index * 3 + 3]
                        color_tuple = (r, g, b)
                        color_name = nearest_colour(color_tuple)
                        if color_name in color_counts:
                            color_counts[color_name] += count
                        else:
                            color_counts[color_name] = count
                    color_info = "\n".join([f"{name}: {count} pixels" for name, count in color_counts.items()])
                    self.query_one("#output", Label).update(f"Colors and their pixel counts:\n{color_info}")
                    
                    self.query_one(ImageViewer).remove()
                    new_viewer = ImageViewer(Image.open(str(to_show)))
                    self.mount(new_viewer, before=self.query_one("#cp"))
            except Exception as e:
                #self.query_one("#output", Label).update("Couldn't load image... Weird.")
                self.query_one("#output", Label).update(str(e))

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
    app = PixCount()
    app.run()