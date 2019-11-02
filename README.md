# GeoLocator

This is a Python package I use for the social media research I am working on where I needed quickly accessible and cacheable geographical data. It currently uses [Nomatim](https://nominatim.org/release-docs/develop/api/Overview/), OpenStreetMaps' API for geolocating addresses through [GeoPy](https://geopy.readthedocs.io/en/stable/).

## Installation

The only pip installable package that GeoLocator depends on is [GeoPy](https://geopy.readthedocs.io/en/stable/), which can be installed in this way:

``` pip install geopy ```

In order to cook down your location to savable addresses, I use another package of my own, [CleanText](https://github.com/kallewesterling/CleanText), which you need to add to your library as well. Installation instructions are available in the README in that repository.

## Usage

GeoLocator is easy to use once you have imported it:

```python
import * from GeoLocator
```

Once it is done, you can call any location with the use of `Location()`:

```python
location = Location("New York City")
```

The resulting object (`location` in this example) has a number of useful things inside it, importantly the geographical data:

```python
print(location.data)
```

The result is a dictionary where you can easily access any information you may need

```python
{'boundingbox': ['40.477399', '40.9161785', '-74.25909', '-73.7001809'],
 'class': 'place',
 'display_name': 'New York, United States of America',
 'geolocator': 'Nominatim',
 'lat': '40.7127281',
 'lng': '-74.0060152',
 'type': 'city'}
```

Note that all of the key-value pairs in this dictionary are also easily accessible through shortcuts such as `location.lat`, `location.lng`, `location.display_name`, and `location.boundingbox`).

## Setting

There is only one setting in the program, which you will find on the top of `GeoLocator.py`.

`LOCATION_CACHE_DIRECTORY` specifies where you want the JSON files saved with the information about your locations.

The default value is a folder called 'locations' in the same folder as the script. Feel free to change it to whatever you'd like.

## Advanced usage

If for some reason you need access to the cache file behind the location, the path is saved in `location.cache.cache_file`.

If you need to load the "live" data from the cache file, you can just call `location.cache.load()` which will return the JSON data as a dictionary, just like the example of `location.data` above.

## Future Features

In the future, I may want to work in ways to implement other geolocators beside [Nomatim](#geolocator). For now I'm happy with it though.