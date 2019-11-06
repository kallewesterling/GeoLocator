
#### Settings #################

LOCATION_CACHE_DIRECTORY = '/Users/kallewesterling/_twitter_cache/geolocated-locations/'
STRICT = False       # New feature: If True, it will crash when it tries to create empty Location objects. If False, allows for empty Location objects.

###############################


import time, json, re, yaml
from random import randint
from pathlib import Path

from geopy import Nominatim
from CleanText import CleanText


class Location():

    def __init__(self, location = None, block = [], replacements = {}, replacements_yaml = None, clean=True):
        stop_all = False

        self.original_location = location

        if clean:
          cleaner = CleanText(location)
          cleaner.digits = False
          cleaner.clean()
          self.clean_location = cleaner.text
        else:
          self.clean_location = location

        self.log = Log()
        self._set_all_empty()
        self.error = False

        if len(block):
            self.clean_location = self.clean_location.split()
            self.clean_location = ' '.join([i for i in self.clean_location if i not in block])
            for w in block:
                if w == self.clean_location: stop_all = True

        if replacements_yaml is not None:
            def replace(match):
                return replacements[match.group(0)]
            with open(replacements_yaml) as f:
                replacements = yaml.safe_load(stream=f)
            if replacements:
                g = re.compile('(%s)' % '|'.join(replacements.keys()))
            self.clean_location = g.sub(replace, self.clean_location)

        if len(self.clean_location) and not stop_all:
          self.cache = LocationCache(self.clean_location)

          if not self.cache.error:
            if not self.cache.data:
                self.data = self.get_data()
                if self.data is None:
                    self.data = {'error': 'not found'}
                    self.log.log(f"Could not find geographic information for location {self.clean_location}")
                self.cache._dump(self.data)
            else:
                self.data = self.cache.data

            if self.data is not None:
              self.lat = self.data.get("lat", None)
              self.lng = self.data.get("lng", None)
              self.geolocator = self.data.get("geolocator", None)
              self._type = self.data.get("type", None)
              self._class = self.data.get("class", None)
              self.display_name = self.data.get("display_name", None)
              self.boundingbox = self.data.get("boundingbox", None)
            else:
              if STRICT:
                raise RuntimeError(f"Data is none in location {location}")
              else:
                self.error = True
                self.data = {'error': 'location empty'}
        elif stop_all:
            self.error = True
            self.data = {'error': 'location manually blocked'}
        else:
          if STRICT:
            raise RuntimeError("Location needs to not be empty.")
          else:
            self.error = True
            self.data = {'error': 'location empty'}


    def _set_all_empty(self):
        self.lat, self.lng, self.geolocator, self._type, self._class, self.display_name, self.boundingbox = None, None, None, None, None, None, None


    def get_data(self, geolocator="Nominatim"):
        if geolocator == "Nominatim":
            self.log.log("Geolocator chosen: Nominatim.")
            _geolocator = Nominatim(user_agent="tags-research-app")
        else:
            raise NotImplementedError("You can currently only use Nomatim as geolocator in this script.")

        try:
            geocoded_location = _geolocator.geocode(self.clean_location)

            sleep_val = randint(2,5)
            self.log.log(f"Sleeping for {sleep_val} seconds...")
            time.sleep(sleep_val)

            if geocoded_location is not None:
                data = {
                    'lat': geocoded_location.raw.get('lat', None),
                    'lng': geocoded_location.raw.get('lon', None),
                    'geolocator': geolocator,
                    'type': geocoded_location.raw.get('type', None),
                    'class': geocoded_location.raw.get('class', None),
                    'display_name': geocoded_location.raw.get('display_name', None),
                    'boundingbox': geocoded_location.raw.get('boundingbox', None)
                }
            else:
                self.error = True
                data = None
        except GeocoderTimedOut:
            if STRICT:
                raise RuntimeError(f"Location {self.clean_location} could not be downloaded. Perhaps you were disconnected?")
            else:
                self.error = True
                data = None

        return(data)


class LocationCache():

    def __init__(self, location):
        self.error = False
        self.location = location
        self.cache_directory = LocationCacheDirectory()
        self.cache_file = self.cache_directory.path / Path(location + ".json")
        if self.cache_file.exists():
            self.data = self.load()
        else:
            self.data = None

    def load(self):
        with open(self.cache_file, 'r') as f:
            data = json.load(f)
        return(data)

    def _dump(self, data):
        if data is None or not isinstance(data, dict): raise RuntimeError("Data must not be empty and must be in dictionary format.")
        try:
            with open(self.cache_file, 'w+') as f:
                json.dump(data, f)
            return(True)
        except:
            return(False)


class LocationCacheDirectory():

    def __init__(self, path = LOCATION_CACHE_DIRECTORY):
        self.path = Path(path)
        self.directory = self.path

        if not self.path.exists(): self.path.mkdir(parents=True) # make sure the cache directory exist
        self._files = None
        self._locations = None

    @property
    def files(self):
        if self._files is None: self._files = self._get_files()
        return(self._files)

    @property
    def locations(self):
        if self._locations is None: self._locations = self._get_locations()
        return(self._locations)

    def _get_files(self):
        return([x for x in self.path.glob("*.json")])

    def _get_locations(self):
        if self._files is None: self._files = self._get_files()
        return([str(x.name).replace(".json", "") for x in self._files])


class Log():

    def __init__(self):
        pass

    def log(self, message = None, level = 0):
        # if level > 0:
        print(message)


def sense_lat_lng_from_name(text):
    g = re.search(r"(-?\d{1,3}\.?\d{0,10}), ?(-?\d{1,3}\.?\d{0,10})", text)
    if g is not None:
        return(g.groups())
    else:
        return(None)