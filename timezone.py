import math

class Timezone:
    def __init__(self, name, country_code, coordinates):
        self.height = 409 # Height of the map
        self.width = 800 # Width of the map
        self.name = name
        self.country_code = country_code
        self.coordinates = coordinates
        latlongsplit = coordinates.find('-', 1)
        if latlongsplit == -1:
            latlongsplit = coordinates.find('+', 1)
        if latlongsplit != -1:
            self.latitude = coordinates[:latlongsplit]
            self.longitude = coordinates[latlongsplit:]
        else:
            self.latitude = coordinates
            self.longitude = '+0'
        
        self.latitude = self.parse_position(self.latitude, 2)
        self.longitude = self.parse_position(self.longitude, 3)
        
        (self.x, self.y) = self.getPosition(self.latitude, self.longitude)            
    
    def parse_position(self, position, wholedigits):
        if position == '' or len(position) < 4 or wholedigits > 9:
            return 0.0
        wholestr = position[:wholedigits + 1]
        fractionstr = position[wholedigits + 1:]
        whole = float(wholestr)
        fraction = float(fractionstr)
        if whole >= 0.0:
            return whole + fraction / pow(10.0, len(fractionstr))
        else:
            return whole - fraction / pow(10.0, len(fractionstr))            
        
    # @return pixel coordinate of a latitude and longitude for self
    # map uses Miller Projection, but is also clipped
    def getPosition(self, la, lo):
        # need to add/sub magic numbers because the map doesn't actually go from -180...180, -90...90
        # thus the upper corner is not -180, -90 and we have to compensate
        # we need a better method of determining the actually range so we can better place citites (shtylman)
        xdeg_offset = -6
        # the 180 - 35) accounts for the fact that the map does not span the entire -90 to 90
        # the map does span the entire 360 though, just offset
        x = (self.width * (180.0 + lo) / 360.0) + (self.width * xdeg_offset/ 180.0)
        x = x % self.width

        #top and bottom clipping latitudes
        topLat = 81
        bottomLat = -59

        #percent of entire possible range
        topPer = topLat/180.0

        # get the y in rectangular coordinates
        y = 1.25 * math.log(math.tan(math.pi/4.0 + 0.4 * math.radians(la)))

        # calculate the map range (smaller than full range because the map is clipped on top and bottom
        fullRange = 4.6068250867599998
        # the amount of the full range devoted to the upper hemisphere
        topOffset = fullRange*topPer
        mapRange = abs(1.25 * math.log(math.tan(math.pi/4.0 + 0.4 * math.radians(bottomLat))) - topOffset)

        # Convert to a percentage of the map range
        y = abs(y - topOffset)
        y = y / mapRange

        # this then becomes the percentage of the height
        y = y * self.height

        return (int(x), int(y))   
