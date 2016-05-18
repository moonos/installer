from gi.repository import Gtk
from utils import Utils

import os

class Handler():
    def __init__(self, builder=None):
        self.builder = builder
        self.utils = Utils(builder)
        self.apply_custom_assistant_button_label()
        
    def mark_as_complete(self, box=None):
        assistant = self.builder.get_object("assistant1")
        vbox = self.builder.get_object(box)
        assistant.set_page_complete(vbox, True)
    
    def commit(self):
        assistant = self.builder.get_object("assistant1")
        assistant.commit()
    
    def apply_custom_assistant_button_label(self):
        # temporarily add a widget to the action area and get its parent
        assistant = self.builder.get_object("assistant1")
        label = Gtk.Label('')
        assistant.add_action_widget(label)
        hbox = label.get_parent()
        hbox.remove(label)
        for child in hbox.get_children():
            label = child.get_label()
            if label == '_Finish' or label == '_Apply':
                child.set_label('Install')
    
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
            elif assistant.get_current_page() == 4:
                self.mark_as_complete("box_user")
                self.utils.setup_user_page_hint()
            elif assistant.get_current_page() == 5:
                self.utils.build_partition_list()
            elif assistant.get_current_page() == 6:
                self.utils.build_slideshow()
                self.commit()
                self.mark_as_complete("box_slideshow")
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
    
    def on_entry_pw_changed(self, editable):
        self.utils.assign_password()
    
    def on_entry_pw_verify_changed(self, editable):
        self.utils.assign_password()
    
    def on_iconview_partition_selection_changed(self, iconview):
        self.utils.iconview_partition_item_selected(iconview)
    
    def on_button_gparted_clicked(self, button):
        os.popen("gparted &")

    def on_button_grub_clicked(self, button):
        self.utils.grub_dialog()
    
    def on_button_refresh_clicked(self, button):
        self.utils.build_partition_list()
