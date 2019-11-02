


#### Settings #################

LOCATION_CACHE_DIRECTORY = '/Users/kallewesterling/_twitter_cache/geolocated-locations/'

###############################


import time, json, re
from random import randint
from pathlib import Path

# dependency
from geopy import Nominatim

# strange dependencies... my own package; needs to be downloaded from GitHub
import CleanText



class LocationCache():

    def __init__(self, location):
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


class Location():

    def __init__(self, location):
        cleaner = CleanText.CleanText(location)
        cleaner.digits = False
        cleaner.clean()

        self.log = Log()

        self.clean_location = cleaner.text

        self.cache = LocationCache(self.clean_location)

        if not self.cache.data:
            self.data = self.get_data()
            if self.data is not None:
                self.cache._dump(self.data)
            else:
                self.log.log(f"Could not find geographic information for location {self.clean_location}")
        else:
            self.data = self.cache.data

        self.lat = self.data.get("lat", None)
        self.lng = self.data.get("lng", None)
        self.geolocator = self.data.get("geolocator", None)
        self._type = self.data.get("type", None)
        self._class = self.data.get("class", None)
        self.display_name = self.data.get("display_name", None)
        self.boundingbox = self.data.get("boundingbox", None)


    def get_data(self, geolocator="Nominatim"):
        if geolocator == "Nominatim":
            self.log.log("Geolocator chosen: Nominatim.")
            sleep_val = randint(2,5)
            self.log.log(f"Sleeping for {sleep_val} seconds...")
            time.sleep(sleep_val)
            _geolocator = Nominatim(user_agent="tags-research-app")
        else:
            raise NotImplementedError("You can currently only use Nomatim as geolocator in this script.")

        try:
            geocoded_location = _geolocator.geocode(self.clean_location)

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
                data = None
        except:
            raise RuntimeError(f"Location {location} could not be downloaded. Perhaps you were disconnected?")

        return(data)


class Log():

    def __init__(self):
        pass

    def log(self, message = None, level = 0):
        # if level > 0:
        print(message)

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