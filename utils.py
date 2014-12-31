from gi.repository import Gtk, Gdk, GdkPixbuf
from PIL import Image
from concurrent import futures

from timezone import Timezone
from setup import Setup
from partition import PartitionSetup

import commands
import os
import subprocess
import parted

class Utils():
    def __init__(self, builder=None):
        self.builder = builder;
        self.renderer = Gtk.CellRendererText()
        self.setup = Setup()
        
    def build_lang_list(self):
        langlist = self.builder.get_object("langlist")
        if langlist.get_column(0) == None:
            model = Gtk.ListStore(str, str)

            langfile = open('data/lang.txt')
            for line in langfile.readlines():
                try:
                    if not line.startswith("#"):
                        col1, col2, language, col4, col5, col6, locale, col8, col9 = line.strip().split(';')
                        iter = model.append((language, locale))
                except:
                    print "Error adding locale '%s'" % line
                    continue

            langlist.set_model(model)
            column = Gtk.TreeViewColumn("Langauges", self.renderer, text=0)
            langlist.append_column(column)

    def build_timezone(self):
        combo_timezones = self.builder.get_object("combobox_timezone")
        
        self.timezone_colors = {}
        self.timezone_colors["2b0000"] = "-11.0"
        self.timezone_colors["550000"] = "-10.0"
        self.timezone_colors["66ff00"] = "-9.5"
        self.timezone_colors["800000"] = "-9.0"
        self.timezone_colors["aa0000"] = "-8.0"
        self.timezone_colors["d40000"] = "-7.0"
        self.timezone_colors["ff0001"] = "-6.0"
        self.timezone_colors["66ff00"] = "-5.5"
        self.timezone_colors["ff2a2a"] = "-5.0"
        self.timezone_colors["c0ff00"] = "-4.5"
        self.timezone_colors["ff5555"] = "-4.0"
        self.timezone_colors["00ff00"] = "-3.5"
        self.timezone_colors["ff8080"] = "-3.0"
        self.timezone_colors["ffaaaa"] = "-2.0"
        self.timezone_colors["ffd5d5"] = "-1.0"
        self.timezone_colors["2b1100"] = "0.0"
        self.timezone_colors["552200"] = "1.0"
        self.timezone_colors["803300"] = "2.0"
        self.timezone_colors["aa4400"] = "3.0"
        self.timezone_colors["00ff66"] = "3.5"
        self.timezone_colors["d45500"] = "4.0"
        self.timezone_colors["00ccff"] = "4.5"
        self.timezone_colors["ff6600"] = "5.0"
        self.timezone_colors["0066ff"] = "5.5"        
        self.timezone_colors["00ffcc"] = "5.75"
        self.timezone_colors["ff7f2a"] = "6.0"
        self.timezone_colors["cc00ff"] = "6.5"
        self.timezone_colors["ff9955"] = "7.0"
        self.timezone_colors["ffb380"] = "8.0"
        self.timezone_colors["ffccaa"] = "9.0"
        self.timezone_colors["a90345"] = "9.5"
        self.timezone_colors["ffe6d5"] = "10.0"
        self.timezone_colors["d10255"] = "10.5"
        self.timezone_colors["d4aa00"] = "11.0"
        self.timezone_colors["fc0266"] = "11.5"
        self.timezone_colors["ffcc00"] = "12.0"
        self.timezone_colors["fd2c80"] = "12.75"
        self.timezone_colors["fc5598"] = "13.0"
            
        #Add some timezones for cities which are located on borders (for which the color doesn't match the color of the rest of the timezone)
        self.timezone_colors["6771a9"] = "5.5" # Calcutta, India
        self.timezone_colors["ff7b7b"] = "-3.0" # Buenos Aires, Argentina
        self.timezone_colors["ff7f7f"] = "-3.0" # Rio Gallegos, Argentina
        self.timezone_colors["d45c27"] = "11.0" # Lord Howe, Australia
        self.timezone_colors["b71f54"] = "10.5" # Adelaide, Australia        
        self.timezone_colors["d29130"] = "-4.0" # Aruba
        self.timezone_colors["ee5f00"] = "4.0" # Baku, Azerbaidjan
        self.timezone_colors["6a2a00"] = "2.0" # Sofia, Bulgaria
        self.timezone_colors["3c1800"] = "" # Porto Novo
        self.timezone_colors["3c1800"] = "1.0" # Benin
        self.timezone_colors["ff9898"] = "-3.0" # Maceio, Brazil
        self.timezone_colors["ff3f3f"] = "-4.0" # Rio Branco, Brazil
        self.timezone_colors["ff802c"] = "6.0" # Thimphu, Bhutan
        self.timezone_colors["ff0000"] = "-6.0" # Belize
        self.timezone_colors["11f709"] = "-3.5" # St Johns, Canada
        self.timezone_colors["e56347"] = "-4.0" # Curacao
        self.timezone_colors["cd5200"] = "4.0" # Tbilisi, Georgia
        self.timezone_colors["2f1300"] = "0.0" # Guernsey. UK
        self.timezone_colors["cea7a3"] = "0.0" # Danmarkshavn, Greenland
        self.timezone_colors["ff2b2b"] = "-4.0" # Thule, Greenland
        self.timezone_colors["79594e"] = "0.0" # Banjul, Gambia
        self.timezone_colors["c7a19d"] = "0.0" # Conakry, Guinea
        self.timezone_colors["5b3e31"] = "0.0" # Bissau, Guinea-Bissau
        self.timezone_colors["3f2314"] = "0.0" # Monrovia, Liberia
        self.timezone_colors["d515db"] = "6.5" # Rangoon, Myanmar
        self.timezone_colors["fd0000"] = "-7.0" # Bahia_Banderas, Mexico
        self.timezone_colors["ffb37f"] = "8.0" # Kuching, Malaysia
        self.timezone_colors["ff0066"] = "11.5" # Norfolk
        self.timezone_colors["351500"] = "1.0" # Lagos, Nigeria
        self.timezone_colors["ff8935"] = "12.75" # Chatham, New Zealand
        self.timezone_colors["913a00"] = "2.0" # Kigali, Rwanda
        self.timezone_colors["ffb17d"] = "8.0" # Singapore
        self.timezone_colors["ddb6b3"] = "0.0" # Freetown, Sierra Leone
        self.timezone_colors["ffb482"] = "9.0" # Dili, East Timor
        self.timezone_colors["ff5599"] = "13.0" # Tongatapu, Tonga
        self.timezone_colors["ff2020"] = "-5.0" # Monticello, USA        
        self.timezone_colors["ff2525"] = "-5.0" # Marengo, USA
        self.timezone_colors["9d0000"] = "-9.0" # Metlakatla, Alaska/USA
        
        self.timezones = []
        model = Gtk.ListStore(str, object)
        _timezones = open("/usr/share/zoneinfo/zone.tab", "r")
        for line in _timezones:
            if not line.strip().startswith("#"):  
                content = line.strip().split("\t")
                if len(content) >= 2:
                    country_code = content[0]
                    coordinates = content[1]
                    timezone = content[2]
                    tz = Timezone(timezone, country_code, coordinates)
                    self.timezones.append(tz)
                    iter = model.append()
                    model.set_value(iter, 0, timezone)
                    model.set_value(iter, 1, tz) 
                    
        combo_timezones.pack_start(self.renderer, True)
        combo_timezones.add_attribute(self.renderer, 'text', 0)
        combo_timezones.set_model(model)
        
        #timezone_map = self.builder.get_object("timezone_map")
        #timezone_map.set_from_file("data/timezone/bg.png")

    def timezone_select(self, timezone):        
        im = Image.open('data/timezone/cc.png')
        rgb_im = im.convert('RGB')
        hexcolor = '%02x%02x%02x' % rgb_im.getpixel((timezone.x, timezone.y))
        print "Color: #%s" % (hexcolor)
        
        overlay_path = "data/timezone/timezone_%s.png" % self.timezone_colors[hexcolor]
        print "Image: %s" % overlay_path
        
        # Superpose the picture of the timezone on the map
        background = Image.open("data/timezone/bg.png")
        dot = Image.open("data/timezone/dot.png")
        overlay = Image.open(overlay_path)
        background = background.convert("RGBA")
        overlay = overlay.convert("RGBA")
        dot = dot.convert("RGBA")
        background.paste(overlay, (0,0), overlay)
        background.paste(dot, (timezone.x-3, timezone.y-3), dot)
        background.save("/tmp/live-installer-map.png","PNG")
        timezone_map = self.builder.get_object("timezone_map")
        timezone_map.set_from_file("/tmp/live-installer-map.png")
        
        # Save the selection
        #self.setup.timezone = timezone.name
        #self.setup.timezone_code = timezone.name
        
    def timezone_combo_selected(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index:
            timezone = model[index][1]
            self.timezone_select(timezone)
                
    def timezone_map_clicked(self, event):
        x = event.x
        y = event.y
        print "Coords: %s %s" % (x, y)
            
        min_distance = 1000 # Looking for min, starting with a large number
        closest_timezone = None
        for timezone in self.timezones:
            distance = abs(x - timezone.x) + abs(y - timezone.y)
            if distance < min_distance:
                min_distance = distance
                closest_timezone = timezone
            
        print "Closest timezone %s" % closest_timezone.name
        self.timezone_select(closest_timezone)
                    
        combo_timezones = self.builder.get_object("combobox_timezone")
        model = combo_timezones.get_model()
        iter = model.get_iter_first()
        while iter is not None:            
            if closest_timezone.name == model.get_value(iter, 1).name:
                combo_timezones.set_active_iter(iter)
                break
            iter = model.iter_next(iter)

    def build_kb_lists(self):
        # Determine the layouts in use
        (keyboard_geom, self.keyboard_layout) = commands.getoutput("setxkbmap -query | awk '/^(model|layout)/{print $2}'").split()
        
        # Build the models
        from collections import defaultdict
        def _ListStore_factory():
            model = Gtk.ListStore(str, str)
            return model
        models = _ListStore_factory()
        layouts = _ListStore_factory()
        variants = defaultdict(_ListStore_factory)
        try:
            import xml.etree.cElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET
        xml = ET.parse('/usr/share/X11/xkb/rules/xorg.xml')
        for node in xml.iterfind('.//modelList/model/configItem'):
            name, desc = node.find('name').text, node.find('description').text
            iterator = models.append((desc, name))
            if name == keyboard_geom:
                self.set_keyboard_model = iterator
        for node in xml.iterfind('.//layoutList/layout'):
            name, desc = node.find('configItem/name').text, node.find('configItem/description').text
            variants[name].append((desc, None))
            for variant in node.iterfind('variantList/variant/configItem'):
                var_name, var_desc = variant.find('name').text, variant.find('description').text
                var_desc = var_desc if var_desc.startswith(desc) else '{} - {}'.format(desc, var_desc)
                variants[name].append((var_desc, var_name))
            iterator = layouts.append((desc, name))
            if name == self.keyboard_layout:
                self.set_keyboard_layout = iterator
                
        self.layout_variants = variants
        
        combobox_keymodel = self.builder.get_object("combobox_keymodel")
        combobox_keymodel.pack_start(self.renderer, True)
        combobox_keymodel.add_attribute(self.renderer, 'text', 0)
        combobox_keymodel.set_model(models)
        try:
            combobox_keymodel.set_active_iter(self.set_keyboard_model)
        except NameError: pass  # set_keyboard_model not set
        
        keylanglist = self.builder.get_object("keylanglist")
        keylanglist.set_model(layouts)
        column = Gtk.TreeViewColumn("Layouts", self.renderer, text=0)
        keylanglist.append_column(column)
        try:
            path = layouts.get_path(set_keyboard_layout)
            keylanglist.set_cursor(path)
            keylanglist.scroll_to_cell(path)
        except NameError: pass  # set_keyboard_layout not set
        
    def assign_keyboard_model(self, combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        (self.keyboard_model_description,
         self.keyboard_model) = model[active]
        print self.keyboard_model
        #os.system('setxkbmap -model ' + self.keyboard_model)
        
    def assign_keyboard_layout(self, selection):
        model, active = selection.get_selected_rows()
        if not active: return
        (self.keyboard_layout_description,
        self.keyboard_layout) = model[active[0]]
        # Set the correct variant list model ...
        model = self.layout_variants[self.keyboard_layout]
        keylangsublist = self.builder.get_object("keylangsublist")
        keylangsublist.set_model(model)
        if keylangsublist.get_column(0) == None:
            column = Gtk.TreeViewColumn("Variants", self.renderer, text=0)
            keylangsublist.append_column(column)
        # ... and select the first variant (standard)
        keylangsublist.set_cursor(0)
    
    def assign_keyboard_variant(self, selection):
        model, active = selection.get_selected_rows()
        if not active: return
        (self.keyboard_variant_description,
         self.keyboard_variant) = model[active[0]]
        if self.keyboard_variant:
            print self.keyboard_variant
            #os.system('setxkbmap -variant ' + self.keyboard_variant)
        else:
            print self.keyboard_layout
            #os.system('setxkbmap -layout ' + self.keyboard_layout)

    def update_preview_cb(self, file_chooser, preview):
        filename = file_chooser.get_preview_filename()
        try:
            if filename:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
                preview.set_from_pixbuf(pixbuf)
                have_preview = True
            else:
                have_preview = False
        except Exception, e:
            have_preview = False
            print e
        file_chooser.set_preview_widget_active(have_preview)
        return  
        
    def face_select_picture_file_chooser(self):
        window = self.builder.get_object("assistant1")
        image = Gtk.Image()
        preview = Gtk.ScrolledWindow()
        preview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        preview.set_size_request(150, 150)
        preview.add_with_viewport(image)
        image.show()
        preview.show()
        chooser = Gtk.FileChooserDialog(title=None, parent=window,
                                        action=Gtk.FileChooserAction.OPEN,
                                        buttons=(Gtk.STOCK_CLOSE,
                                                 Gtk.ResponseType.CANCEL,
                                                 Gtk.STOCK_OPEN,
                                                 Gtk.ResponseType.OK))
        chooser.set_default_response(Gtk.ResponseType.OK)
        chooser.set_current_folder("/usr/share/pixmaps/faces")

        filter = Gtk.FileFilter()
        filter.set_name('Images')
        filter.add_mime_type('image/png')
        filter.add_mime_type('image/jpeg')
        filter.add_mime_type('image/gif')
        filter.add_mime_type('bitmap/bmp')        
        chooser.add_filter(filter)        
        chooser.set_preview_widget(preview)
        chooser.connect("update-preview", self.update_preview_cb, image)
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            os.system("convert '%s' -resize x96 /tmp/live-installer-face.png" % filename)
            image_user = self.builder.get_object("image_user")
            image_user.set_from_file("/tmp/live-installer-face.png")
        chooser.destroy()

    def face_select_picture(self):
        window = self.builder.get_object("assistant1")
        
        # use local builder to reset glade reference
        builder = Gtk.Builder()
        builder.add_from_file("data/moonos_installer.ui")
        
        liststore = Gtk.ListStore(GdkPixbuf.Pixbuf)
        
        iconview = builder.get_object("iconview_username")
        iconview.set_model(liststore)
        iconview.set_pixbuf_column(0)
        
        path = "/usr/share/pixmaps/faces"
        listimg = os.listdir(path)
        for img in listimg:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(path, img))
            liststore.append([pixbuf])
        
        chooser = builder.get_object("messagedialog_userimage")
        chooser.set_default_response(Gtk.ResponseType.OK)
        chooser.set_transient_for(window)
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            position = iconview.get_selected_items()[0]
            img = listimg[int(position.to_string())]
            filename = os.path.join(path, img)
            os.system("convert '%s' -resize x96 /tmp/live-installer-face.png" % filename)
            image_user = self.builder.get_object("image_user")
            image_user.set_from_file("/tmp/live-installer-face.png")
        chooser.destroy()

    def assign_password(self):
        entry_pw = self.builder.get_object("entry_pw")
        entry_pw_verify = self.builder.get_object("entry_pw_verify")
        label_pw = self.builder.get_object("label_pw")
        
        self.password = entry_pw.get_text()
        self.password_verify = entry_pw_verify.get_text()
        
        if(self.password == "" and self.password_verify == ""):
            label_pw.hide()
        else:
            label_pw.show()
            
        if (self.password != self.password_verify):
            label_pw.set_label("Passwords not match.")
        else:
            label_pw.set_label("Passwords match.")

    def build_hdds(self):
        self.setup.disks = []
        output = subprocess.Popen("lsblk -nrdo TYPE,NAME,SIZE,RM | grep ^disk", shell=True, stdout=subprocess.PIPE)
        for line in output.stdout:
            line = line.rstrip("\r\n")
            sections = line.split(" ")
            if len(sections) == 4:
                dev_name = sections[1]
                dev_size = sections[2]
                dev_removable = sections[3]
                dev_path = "/dev/%s" % dev_name
                if dev_removable == "0":
                    self.setup.disks.append(dev_path)
            else:
                print "WARNING, erroneous info collected for disks. Please show this to the development team: %s" % line
                
    def build_partition_model(self):
        liststore = []
        
        self.build_hdds()
        
        os.popen('mkdir -p /tmp/live-installer/tmpmount')
        
        try:
            self.setup.partitions = []
            os.system("modprobe efivars >/dev/null 2>&1")
            if os.path.exists("/proc/efi") or os.path.exists("/sys/firmware/efi"):
                self.setup.gptonefi = True
            for hdd in self.setup.disks:
                device = parted.getDevice(hdd)
                try:
                    disk = parted.Disk(device)
                except Exception:
                    raise
                partition = disk.getFirstPartition()
                last_added_partition = PartitionSetup(partition)
                partition = partition.nextPartition()
                while (partition is not None):
                    if last_added_partition.partition.number == -1 and partition.number == -1:
                        last_added_partition.add_partition(partition)
                    else:                        
                        last_added_partition = PartitionSetup(partition) 
                        if "swap" in last_added_partition.type:
                            last_added_partition.type = "swap"
                            last_added_partition.description = "swap"
                        
                        #if partition.number != -1 and "swap" not in last_added_partition.type and partition.type != parted.PARTITION_EXTENDED:
                            #Umount temp folder
                        #    if ('/tmp/live-installer/tmpmount' in commands.getoutput('mount')):
                        #        os.popen('umount /tmp/live-installer/tmpmount')

                            #Mount partition if not mounted
                        #    if (partition.path not in commands.getoutput('mount')):                                
                        #        os.system("mount %s /tmp/live-installer/tmpmount" % partition.path)
                            
                            #Identify partition's description and used space
                        #    if (partition.path in commands.getoutput('mount')):
                        #        df_lines = commands.getoutput("df 2>/dev/null | grep %s" % partition.path).split('\n')
                        #        for df_line in df_lines:
                        #            df_elements = df_line.split()
                        #            if df_elements[0] == partition.path:
                        #                last_added_partition.used_space = df_elements[4]  
                        #                mount_point = df_elements[5]                              
                        #                if "%" in last_added_partition.used_space:
                        #                    used_space_pct = int(last_added_partition.used_space.replace("%", "").strip())
                        #                    last_added_partition.free_space = int(float(last_added_partition.size) * (float(100) - float(used_space_pct)) / float(100))                                            
                        #            break
                        #    else:
                        #        print "Failed to mount %s" % partition.path

                            
                            #Umount temp folder
                        #    if ('/tmp/live-installer/tmpmount' in commands.getoutput('mount')):
                        #        os.popen('umount /tmp/live-installer/tmpmount') 
                                
                    if last_added_partition.size > 1.0:
                        display_name = last_added_partition.label
                        path = last_added_partition.name
                        if last_added_partition.type == "ext3":
                            liststore.append([display_name, path])
                        elif last_added_partition.type == "ext4":
                            liststore.append([display_name, path])
                    
                    partition = partition.nextPartition()
        except Exception, detail:
            print detail
        
        return liststore
            
    def set_cursor(self, cursor):
        window = self.builder.get_object("assistant1")
        if cursor == "busy":
            window.set_sensitive(False)
            cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
            window.get_root_window().set_cursor(cursor)
        else:
            window.set_sensitive(True)
            cursor = Gdk.Cursor(Gdk.CursorType.ARROW)
            window.get_root_window().set_cursor(cursor) 
        
    def build_partition_listview(self, future):
        label_target_disk = self.builder.get_object("label_target_disk")
        label_target_disk.set_label("")
        
        if len(future.result()) == 0:
            label_target_disk.set_label("Error")
        else:
            liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
            for display_name, path in future.result():
                pixbuf = Gtk.IconTheme.get_default().load_icon("drive-harddisk", 96, 0)
                liststore.append([pixbuf, display_name, path])
            
            iconview = self.builder.get_object("iconview_partition")
            iconview.set_model(liststore)
            iconview.set_pixbuf_column(0)
            iconview.set_text_column(1)
        
        self.set_cursor("normal")
        
    def build_partition_list(self): 
        self.set_cursor("busy")
        executor = futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self.build_partition_model)
        future.add_done_callback(self.build_partition_listview)
        
    def iconview_partition_item_selected(self, iconview):
        label_target_disk = self.builder.get_object("label_target_disk")
        label_target_disk.show()
        
        path = iconview.get_selected_items()
        liststore = iconview.get_model()
        treeiter = liststore.get_iter(path)
        
        display_name = liststore.get_value(treeiter, 1)
        path = liststore.get_value(treeiter, 2)
        
        text = "moonOS will installed on the disk \"%s\"" % display_name
        label_target_disk.set_label(text)
