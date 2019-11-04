# GeoLocator

This is a Python package I use for the social media research I am working on where I needed quickly accessible and cacheable geographical data. It currently uses [Nomatim](https://nominatim.org/release-docs/develop/api/Overview/), OpenStreetMaps' API for geolocating addresses through [GeoPy](https://geopy.readthedocs.io/en/stable/).

## Installation

There are two pip installable packages that GeoLocator depends on: 
- [GeoPy](https://geopy.readthedocs.io/en/stable/)
- [PyYAML](https://pyyaml.org/wiki/PyYAML)

Both can be installed like so:

``` pip install --upgrade geopy ```
``` pip install --upgrade yaml ```

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

## Optional arguments

The program comes with a number of helpers in the construction of the Location object.

### 1. `block`

Adding a `block` argument to the `Location` constructor allows you to remove words from the location name, thus making it easier for the geolocator to find correct location and coordinates.

If you add single words in the list, they will be removed individually from the name. If there are several words in the list entry, those will also be matched against the whole name of the location, and be blocked altogether.

As an example, try running these two geolocators, and print the resulting `clean_location` (which is what your input generates for the geolocator to see):

```python
location = Location("I live in New York City")
print(location.clean_location)

location = Location("I live in New York City", block=['live'])
print(location.clean_location)
```

You should see two outputs; the first one containing the word `live` and the next one without the word:

```python
live new york city
```

```python
new york city
```

Looking deeper at the results by investigating the `location.data` dictionary for each of the two, we will see that they differ vastly:

```python
{'boundingbox': ['40.7748081', '40.7749081', '-73.9537456', '-73.9536456'],
 'class': 'amenity',
 'display_name': 'Comic Strip Live, 1568, 2nd Avenue, Franklin Plaza, Lenox '
                 'Hill, Manhattan Community Board 8, Manhattan, New York '
                 'County, New York, 10028, United States of America',
 'geolocator': 'Nominatim',
 'lat': '40.7748581',
 'lng': '-73.9536956',
 'type': 'theatre'}
```

```python
{'boundingbox': ['40.477399', '40.9161785', '-74.25909', '-73.7001809'],
 'class': 'place',
 'display_name': 'New York, United States of America',
 'geolocator': 'Nominatim',
 'lat': '40.7127281',
 'lng': '-74.0060152',
 'type': 'city'}
```

### 2. `replacements`

If there are parts of any location that you want to replace with another string, you can do so by either providing a dictionary or a YAML file with a "mapping" (see 3 below). It is easy to provide a short dictionary if you only have a few values you want to replace:

```python
location = Location("I live in NYC", replacements={'NYC': 'New York City'})
print(location.clean_location)
```

*Note that it does not matter whether you enter your replacements in lowercase, uppercase or mixed case - it will all be lowercased anyway.*

This should provide you with the following string:

```python
live new york city
```

You can, of course, combine it with the block list from (1) above as well:

```python
location = Location("I live in NYC", block=['live'], replacements={'NYC': 'New York City'})
pprint(location.clean_location)
```

```python
new york city
```

### 3. `replacements_yaml`

If you have many replacements, it might not be nice to have an excessively long line in your script. That is when `replacements_yaml` comes in handy. You can simply provide the script a string with a path to a YAML file that contains your mappings.

In this example, we have put the following into a `./configuration/location_mapping.yml` file:

```yaml
"ldn": "london"
"americaa": "america"
"atl": "atlanta"
"lfk": "lawrence kansas"
"kcmo": "kansas city missouri"
```

*If you are unsure how to format a YAML document, it is suggested that you use a [YAML linter](http://www.yamllint.com/) before linking up your document to your script.*

In the script, we add a string with the path to our `replacements_yaml`:

```python
location = Location("I love ldn", block=['love'], replacements_yaml='./configuration/location_mapping.yml')
print(location.clean_location)
```

The result:

```python
london
```

## Base settings

There are only a few settings for the program. You will find settings in the first few lines at the top of `GeoLocator.py`:

| Setting        | Type | Controls
| ------------- | ------------- | ------------- |
| `LOCATION_CACHE_DIRECTORY` | path to directory (`str` or `Path`) | Specifies where you want the JSON files saved with the information about your locations. (Default is `./locations/`.)
| `STRICT` | `True` or `False` (`bool`) | Specifies whether you want the script to be lenient and not crash as easily. (Default is `False`.)

## Advanced usage

If for some reason you need access to the cache file behind the location, the path is saved in `location.cache.cache_file`.

If you need to load the "live" data from the cache file, you can just call `location.cache.load()` which will return the JSON data as a dictionary, just like the example of `location.data` above.

## Future Features

In the future, I may want to work in ways to implement other geolocators beside [Nomatim](#geolocator). For now I'm happy with it though.