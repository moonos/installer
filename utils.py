from gi.repository import Gtk
from PIL import Image

from timezone import Timezone

timezones = []
timezone_colors = {}

def build_lang_list(builder=None):
    langlist = builder.get_object("langlist")
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
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Langauges  ", renderer, text=0)
        langlist.append_column(column)

def build_timezone(builder=None):
    combo_timezones = builder.get_object("combobox_timezone")
    
    global timezone_colors
    timezone_colors["2b0000"] = "-11.0"
    timezone_colors["550000"] = "-10.0"
    timezone_colors["66ff00"] = "-9.5"
    timezone_colors["800000"] = "-9.0"
    timezone_colors["aa0000"] = "-8.0"
    timezone_colors["d40000"] = "-7.0"
    timezone_colors["ff0001"] = "-6.0"
    timezone_colors["66ff00"] = "-5.5"
    timezone_colors["ff2a2a"] = "-5.0"
    timezone_colors["c0ff00"] = "-4.5"
    timezone_colors["ff5555"] = "-4.0"
    timezone_colors["00ff00"] = "-3.5"
    timezone_colors["ff8080"] = "-3.0"
    timezone_colors["ffaaaa"] = "-2.0"
    timezone_colors["ffd5d5"] = "-1.0"
    timezone_colors["2b1100"] = "0.0"
    timezone_colors["552200"] = "1.0"
    timezone_colors["803300"] = "2.0"
    timezone_colors["aa4400"] = "3.0"
    timezone_colors["00ff66"] = "3.5"
    timezone_colors["d45500"] = "4.0"
    timezone_colors["00ccff"] = "4.5"
    timezone_colors["ff6600"] = "5.0"
    timezone_colors["0066ff"] = "5.5"        
    timezone_colors["00ffcc"] = "5.75"
    timezone_colors["ff7f2a"] = "6.0"
    timezone_colors["cc00ff"] = "6.5"
    timezone_colors["ff9955"] = "7.0"
    timezone_colors["ffb380"] = "8.0"
    timezone_colors["ffccaa"] = "9.0"
    timezone_colors["a90345"] = "9.5"
    timezone_colors["ffe6d5"] = "10.0"
    timezone_colors["d10255"] = "10.5"
    timezone_colors["d4aa00"] = "11.0"
    timezone_colors["fc0266"] = "11.5"
    timezone_colors["ffcc00"] = "12.0"
    timezone_colors["fd2c80"] = "12.75"
    timezone_colors["fc5598"] = "13.0"
        
    #Add some timezones for cities which are located on borders (for which the color doesn't match the color of the rest of the timezone)
    timezone_colors["6771a9"] = "5.5" # Calcutta, India
    timezone_colors["ff7b7b"] = "-3.0" # Buenos Aires, Argentina
    timezone_colors["ff7f7f"] = "-3.0" # Rio Gallegos, Argentina
    timezone_colors["d45c27"] = "11.0" # Lord Howe, Australia
    timezone_colors["b71f54"] = "10.5" # Adelaide, Australia        
    timezone_colors["d29130"] = "-4.0" # Aruba
    timezone_colors["ee5f00"] = "4.0" # Baku, Azerbaidjan
    timezone_colors["6a2a00"] = "2.0" # Sofia, Bulgaria
    timezone_colors["3c1800"] = "" # Porto Novo
    timezone_colors["3c1800"] = "1.0" # Benin
    timezone_colors["ff9898"] = "-3.0" # Maceio, Brazil
    timezone_colors["ff3f3f"] = "-4.0" # Rio Branco, Brazil
    timezone_colors["ff802c"] = "6.0" # Thimphu, Bhutan
    timezone_colors["ff0000"] = "-6.0" # Belize
    timezone_colors["11f709"] = "-3.5" # St Johns, Canada
    timezone_colors["e56347"] = "-4.0" # Curacao
    timezone_colors["cd5200"] = "4.0" # Tbilisi, Georgia
    timezone_colors["2f1300"] = "0.0" # Guernsey. UK
    timezone_colors["cea7a3"] = "0.0" # Danmarkshavn, Greenland
    timezone_colors["ff2b2b"] = "-4.0" # Thule, Greenland
    timezone_colors["79594e"] = "0.0" # Banjul, Gambia
    timezone_colors["c7a19d"] = "0.0" # Conakry, Guinea
    timezone_colors["5b3e31"] = "0.0" # Bissau, Guinea-Bissau
    timezone_colors["3f2314"] = "0.0" # Monrovia, Liberia
    timezone_colors["d515db"] = "6.5" # Rangoon, Myanmar
    timezone_colors["fd0000"] = "-7.0" # Bahia_Banderas, Mexico
    timezone_colors["ffb37f"] = "8.0" # Kuching, Malaysia
    timezone_colors["ff0066"] = "11.5" # Norfolk
    timezone_colors["351500"] = "1.0" # Lagos, Nigeria
    timezone_colors["ff8935"] = "12.75" # Chatham, New Zealand
    timezone_colors["913a00"] = "2.0" # Kigali, Rwanda
    timezone_colors["ffb17d"] = "8.0" # Singapore
    timezone_colors["ddb6b3"] = "0.0" # Freetown, Sierra Leone
    timezone_colors["ffb482"] = "9.0" # Dili, East Timor
    timezone_colors["ff5599"] = "13.0" # Tongatapu, Tonga
    timezone_colors["ff2020"] = "-5.0" # Monticello, USA        
    timezone_colors["ff2525"] = "-5.0" # Marengo, USA
    timezone_colors["9d0000"] = "-9.0" # Metlakatla, Alaska/USA
    
    global timezones
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
                timezones.append(tz)
                iter = model.append()
                model.set_value(iter, 0, timezone)
                model.set_value(iter, 1, tz) 
                
    renderer = Gtk.CellRendererText()
    combo_timezones.pack_start(renderer, True)
    combo_timezones.add_attribute(renderer, 'text', 0)
    combo_timezones.set_model(model)
    
    #timezone_map = builder.get_object("timezone_map")
    #timezone_map.set_from_file("data/timezone/bg.png")

def timezone_select(builder=None, timezone=None):        
    im = Image.open('data/timezone/cc.png')
    rgb_im = im.convert('RGB')
    hexcolor = '%02x%02x%02x' % rgb_im.getpixel((timezone.x, timezone.y))
    print "Color: #%s" % (hexcolor)
    
    overlay_path = "data/timezone/timezone_%s.png" % timezone_colors[hexcolor]
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
    timezone_map = builder.get_object("timezone_map")
    timezone_map.set_from_file("/tmp/live-installer-map.png")
    
    # Save the selection
    #self.setup.timezone = timezone.name
    #self.setup.timezone_code = timezone.name
    
def timezone_combo_selected(builder=None, combobox=None):
    model = combobox.get_model()
    index = combobox.get_active()
    if index:
        timezone = model[index][1]
        timezone_select(builder, timezone)
            
def timezone_map_clicked(builder=None, event=None):
    x = event.x
    y = event.y
    print "Coords: %s %s" % (x, y)
        
    min_distance = 1000 # Looking for min, starting with a large number
    closest_timezone = None
    for timezone in timezones:
        distance = abs(x - timezone.x) + abs(y - timezone.y)
        if distance < min_distance:
            min_distance = distance
            closest_timezone = timezone
        
    print "Closest timezone %s" % closest_timezone.name
    timezone_select(builder, closest_timezone)
                
    combo_timezones = builder.get_object("combobox_timezone")
    model = combo_timezones.get_model()
    iter = model.get_iter_first()
    while iter is not None:            
        if closest_timezone.name == model.get_value(iter, 1).name:
            combo_timezones.set_active_iter(iter)
            break
        iter = model.iter_next(iter)


