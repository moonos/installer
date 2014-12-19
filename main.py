#!/usr/bin/env python

from gi.repository import Gtk, WebKit
from handler import Handler

builder = Gtk.Builder()
builder.add_from_file("data/moonos_installer.ui")
builder.connect_signals(Handler(builder))

window = builder.get_object("assistant1")
window.show_all()

Gtk.main()
