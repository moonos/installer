from gi.repository import Gtk, Gdk
from utils import Utils

class Handler():
    def __init__(self, builder=None):
        self.builder = builder
        self.utils = Utils(builder)
        
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
                self.utils.build_lang_list()
            elif assistant.get_current_page() == 2:
                self.utils.build_kb_lists()
            elif assistant.get_current_page() == 3:
                self.utils.build_timezone()
            elif assistant.get_current_page() == 5:
                assistant.set_sensitive(False)
                cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
                assistant.get_window().set_cursor(cursor) 
                self.utils.build_partition_list()
        else:
            print "already initialized"
        
    def on_treeview_selection1_changed(self, selection):
        self.mark_as_complete("box_language")
    
    def on_timezone_event_button_release_event(self, widget, event):
        self.utils.timezone_map_clicked(event)
    
    def on_combobox_timezone_changed(self, combobox):
        self.utils.timezone_combo_selected(combobox)
        self.mark_as_complete("box_timezone")
    
    def on_keylanglist_selection_changed(self, selection):
        self.utils.assign_keyboard_layout(selection)
        self.mark_as_complete("box_keyboard")
    
    def on_combobox_keymodel_changed(self, combobox):
        self.utils.assign_keyboard_model(combobox)
        self.mark_as_complete("box_keyboard")
    
    def on_keylangsublist_selection_changed(self, selection):
        self.utils.assign_keyboard_variant(selection)
        self.mark_as_complete("box_keyboard")
    
    def on_button_user_clicked(self, button):
        self.utils.face_select_picture()
        self.mark_as_complete("box_user")
    
    def on_entry_pw_changed(self, editable):
        self.utils.assign_password()
    
    def on_entry_pw_verify_changed(self, editable):
        self.utils.assign_password()
    
    def on_iconview_partition_selection_changed(self, iconview):
        self.utils.iconview_partition_item_selected(iconview)
