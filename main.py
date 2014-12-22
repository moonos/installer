#!/usr/bin/env python

from gi.repository import Gtk, Gdk
from handler import Handler

builder = Gtk.Builder()
builder.add_from_file("data/moonos_installer.ui")
builder.connect_signals(Handler(builder))

style_provider = Gtk.CssProvider()

css = open('data/style.css')
css_data = css.read()
css.close()

style_provider.load_from_data(css_data)

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window = builder.get_object("assistant1")
window.show_all()

Gtk.main()
