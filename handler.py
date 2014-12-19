from gi.repository import Gtk
import utils

class Handler():
    def __init__(self, builder=None):
        self.builder = builder;
        
    def mark_as_complete(self, box=None):
        assistant = self.builder.get_object("assistant1")
        vbox = self.builder.get_object(box)
        assistant.set_page_complete(vbox, True)
    
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def on_assistant1_cancel(self, assistant):
        Gtk.main_quit()
        
    def on_assistant1_close(self, assistant):
        Gtk.main_quit()
        
    def on_assistant1_apply(self, assistant):
        print "hello"
    
    def on_assistant1_prepare(self, assistant, page):
        if not assistant.get_page_complete(page):
            if assistant.get_current_page() == 1:
                utils.build_lang_list(self.builder)
            elif assistant.get_current_page() == 3:
                utils.build_timezone(self.builder)
        else:
            print "already initialized"
        
    def on_treeview_selection1_changed(self, selection):
        self.mark_as_complete("box_language")
    
    def on_timezone_event_button_release_event(self, widget, event):
        utils.timezone_map_clicked(self.builder, event)
    
    def on_combobox_timezone_changed(self, combobox):
        utils.timezone_combo_selected(self.builder, combobox)
        self.mark_as_complete("box_timezone")
