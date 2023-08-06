
# Mimeo (Mimeograph)

**Mimeo** is a command line tool and python library generating custom data based on a template.
It can be used by developers, testers or even business analysts in their daily work.


## Installation

Install Mimeo with pip

```sh
pip install mimeograph
```


## Usage/Examples

### Mimeo Configuration

Prepare Mimeo Configuration first
- for a command line tool: in a JSON file
- for a `Mimeograph` python class: in a `dict`

```json
{
  "_templates_": [
    {
      "count": 30,
      "model": {
        "SomeEntity": {
          "_attrs": {
            "xmlns": "http://mimeo.arch.com/default-namespace",
            "xmlns:pn": "http://mimeo.arch.com/prefixed-namespace"
          },
          "ChildNode1": 1,
          "ChildNode2": "value-2",
          "ChildNode3": true
        }
      }
    }
  ]
}
```
_You can find more configuration examples in the `examples` folder._

### Mimeograph

#### Command line tool

```sh
mimeo SomeEntity-config.json
```

#### Python library

```python
from mimeo import Mimeograph
from mimeo.config import MimeoConfig

config = {
    # Your configuration
}
mimeo_config = MimeoConfig(config)
Mimeograph(mimeo_config).produce()
```
***
The Mimeo Configuration above will produce 2 files:

```xml
<!-- mimeo-output/mimeo-output-1.xml-->
<SomeEntity xmlns="http://mimeo.arch.com/default-namespace" xmlns:pn="http://mimeo.arch.com/prefixed-namespace">
    <ChildNode1>1</ChildNode1>
    <ChildNode2>value-2</ChildNode2>
    <ChildNode3>true</ChildNode3>
</SomeEntity>
```
```xml
<!-- mimeo-output/mimeo-output-2.xml-->
<SomeEntity xmlns="http://mimeo.arch.com/default-namespace" xmlns:pn="http://mimeo.arch.com/prefixed-namespace">
    <ChildNode1>1</ChildNode1>
    <ChildNode2>value-2</ChildNode2>
    <ChildNode3>true</ChildNode3>
</SomeEntity>
```
***

### Mimeo Utils

Mimeo exposes several functions for data generation that will make it more useful for testing purposes.

**Template**
```json
{
  "count": 2,
  "model": {
    "SomeEntity": {
      "id": "{auto_increment()}",
      "randomstring": "{random_str()}",
      "randomint": "{random_int()}",
    }
  }
}
```

**XML Data**
```xml
<SomeEntity>
    <id>00001</id>
    <randomstring>mCApsYZprayYkmKnYWxe</randomstring>
    <randomint>8</randomint>
</SomeEntity>
```
```xml
<SomeEntity>
    <id>00002</id>
    <randomstring>ceaPUqARUkFukZIPeuqO</randomstring>
    <randomint>99</randomint>
</SomeEntity>
```


## Documentation

### Mimeo Configuration

Mimeo configuration is defined in a JSON file using internal settings and data templates.

| Key                             |  Level   |      Required      |     Supported values     |    Default     | Description                                                                                                                                             |
|:--------------------------------|:--------:|:------------------:|:------------------------:|:--------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `output_format`                 |  Config  |        :x:         |          `xml`           |     `xml`      | Defines output data format                                                                                                                              |
| `output_details`                |  Config  |        :x:         |          object          |      ---       | Defines output details on how it will be consumed                                                                                                       |
| `output_details/direction`      |  Config  |        :x:         | `file`, `stdout`, `http` |     `file`     | Defines how output will be consumed                                                                                                                     |
| `output_details/directory_path` |  Config  |        :x:         |          string          | `mimeo-output` | For `file` direction - defines an output directory                                                                                                      |
| `output_details/file_name`      |  Config  |        :x:         |          string          | `mimeo-output` | For `file` direction - defines an output file name                                                                                                      |
| `output_details/method`         |  Config  |        :x:         |      `POST`, `PUT`       |     `POST`     | For `http` direction - defines a request method                                                                                                         |
| `output_details/protocol`       |  Config  |        :x:         |     `http`, `https`      |     `http`     | For `http` direction - defines a url protocol                                                                                                           |
| `output_details/host`           |  Config  | :heavy_check_mark: |          string          |      ---       | For `http` direction - defines a url host                                                                                                               |
| `output_details/port`           |  Config  |        :x:         |         integer          |     `null`     | For `http` direction - defines a url port (can be empty)                                                                                                |
| `output_details/endpoint`       |  Config  | :heavy_check_mark: |          string          |      ---       | For `http` direction - defines a url endpoint                                                                                                           |
| `output_details/auth`           |  Config  |        :x:         |    `basic`, `digest`     |    `basic`     | For `http` direction - defines a auth method                                                                                                            |
| `output_details/username`       |  Config  | :heavy_check_mark: |          string          |      ---       | For `http` direction - defines a username                                                                                                               |
| `output_details/password`       |  Config  | :heavy_check_mark: |          string          |      ---       | For `http` direction - defines a password                                                                                                               |
| `indent`                        |  Config  |        :x:         |         integer          |     `null`     | Defines indent applied in output data                                                                                                                   |
| `vars`                          |  Config  |        :x:         |          object          |      ---       | Defines variables to be used in a Mimeo Template (read more in next section)                                                                            |
| `xml_declaration`               |  Config  |        :x:         |         boolean          |    `false`     | Indicates whether an xml declaration should be added to output data                                                                                     |
| `_templates_`                   |  Config  | :heavy_check_mark: |          array           |      ---       | Stores templates for data generation                                                                                                                    |
| `count`                         | Template | :heavy_check_mark: |         integer          |      ---       | Indicates number of copies                                                                                                                              |
| `model`                         | Template | :heavy_check_mark: |          object          |      ---       | Defines data template to be copied                                                                                                                      |
| `context`                       |  Model   |        :x:         |          object          |      ---       | Defines a context name that is internally used e.g. using `curr_iter()` and `get_key()` mimeo utils (by default model name is used as the context name) |

#### Mimeo Vars

Mimeo allows you to define a list of variables.
You can use them in your Mimeo Config by wrapping them in curly brackets [`{VARIABLE}`].

There are only 2 rules for variable names:
- Variable name can include upper-cased letters \[`A-Z`\], underscore \[`_`\] and digits \{`0-9`\} only
- Variable name must start with a letter

Variable can be defined with:
- any atomic value
- any other variable defined
- any Mimeo Util

You can use Mimeo Vars as partial values (unless they are defined as Mimeo Utils).

Example:
```json
{
  "vars": {
    "CUSTOM_VAR_1": "custom-value-1",
    "CUSTOM_VAR_2": 1,
    "CUSTOM_VAR_3": true,
    "CUSTOM_VAR_4": "{CUSTOM_VAR_2}",
    "CUSTOM_VAR_5": "{auto_increment('{}')}"
  },
  "_templates_": [
    {
      "count": 5,
      "model": {
        "SomeEntity": {
          "ChildNode1": "{CUSTOM_VAR_1}",
          "ChildNode2": "{CUSTOM_VAR_2}",
          "ChildNode3": "{CUSTOM_VAR_3}",
          "ChildNode4": "{CUSTOM_VAR_4}",
          "ChildNode5": "{CUSTOM_VAR_5}",
          "ChildNode6": "{CUSTOM_VAR_1}-with-suffix"
        }
      }
    }
  ]
}
```

#### Mimeo Special Fields

In Mimeo Template you can use so-called _special fields_.
Every field in a template can be stored in memory (_provided_) and used later as a value of other fields (_injected_).
To provide and inject a special field use curly brackets and colons: [`{:SomeField:}`].
You provide a field when you use this format in a field name (JSON property name),
and inject by applying it in a field value.  
They can be injected as partial values, similarly to Mimeo Vars.

Example
```json
{
  "_templates_": [
    {
      "count": 5,
      "model": {
        "SomeEntity": {
          "{:ChildNode1:}": "custom-value",
          "ChildNode2": "{:ChildNode1:}",
          "ChildNode3": "{:ChildNode1:}-with-suffix"
        }
      }
    }
  ]
}
```

### Mimeo CLI

#### Mimeo Configuration arguments

When using Mimeo command line tool you can overwrite Mimeo Configuration properties:

| Short option | Long option         | Description                                                                          |
|:------------:|:--------------------|:-------------------------------------------------------------------------------------|
|     `-x`     | `--xml-declaration` | overwrite the `xml_declaration` property                                             |
|     `-i`     | `--indent`          | overwrite the `indent` property                                                      |
|     `-o`     | `--output`          | overwrite the `output_details/direction` property                                    |
|     `-d`     | `--directory`       | overwrite the `output_details/directory_path` property                               |
|     `-f`     | `--file`            | overwrite the `output_details/file_name` property                                    |
|     `-H`     | `--http-host`       | overwrite the `output_details/host` property                                         |
|     `-p`     | `--http-port`       | overwrite the `output_details/port` property                                         |
|     `-E`     | `--http-endpoint`   | overwrite the `output_details/endpoint` property                                     |
|     `-U`     | `--http-user`       | overwrite the `output_details/username` property                                     |
|     `-P`     | `--http-password`   | overwrite the `output_details/password` property                                     |
|              | `--http-method`     | overwrite the `output_details/method` property                                       |
|              | `--http-protocol`   | overwrite the `output_details/protocol` property                                     |
|              | `--http-auth`       | overwrite the `output_details/auth` property                                         |
|     `-e`     | `--http-env`        | overwrite the output_details http properties using a mimeo environment configuration |
|              | `--http-envs-file`  | use a custom environments file (by default: mimeo.envs.json)                         |

#### Logging arguments

| Short option | Long option | Description       |
|:------------:|:------------|:------------------|
|              | `--silent`  | disable INFO logs |
|              | `--debug`   | enable DEBUG mode |
|              | `--fine`    | enable FINE mode  |

### Mimeo Utils

You can use several predefined functions to generate data by using them within curly braces:
```xml
<id>{auto_increment()}</id>
```

| Function                                                                   | Example                                 | Data                                                                                                                       |
|:---------------------------------------------------------------------------|:----------------------------------------|:---------------------------------------------------------------------------------------------------------------------------|
| `auto_increment()`                                                         |                                         | Generates next integer in context of a model (in nested templates it will use a separated context)                         |
| `auto_increment(<STRING_PATTERN>)`                                         | `auto_increment('MYID{:010d}')`         | Same as `auto_increment()` but the integer is used in a string pattern provided                                            |
| `curr_iter()`                                                              |                                         | Generates a value of the current iteration in a Mimeo Template context                                                     |
| `curr_iter(<CONTEXT_NAME>)`                                                | `curr_iter('SomeEntity')`               | Generates a value of the current iteration in a specific Mimeo Model context (model name when `context` is not configured) |
| `key()`                                                                    |                                         | Generates a key unique across all Mimeo Models and being the same within a single Mimeo Model context                      |
| `get_key(<CONTEXT_NAME>)`                                                  | `get_key('SomeEntity')`                 | Retrieves the last key from a specific context  (model name when `context` is not configured)                              |
| `get_key(<CONTEXT_NAME>, <ITERATION>)`                                     | `get_key('SomeEntity', 5)`              | Retrieves a key from a specific context (model name when `context` is not configured) and from a specific iteration        |
| `random_str()`                                                             |                                         | Generates a random string value of the default length: 20 characters                                                       |
| `random_str(<LENGTH>)`                                                     | `random_str(2)`                         | Generates a random string value of the customized length                                                                   |
| `random_int()`                                                             |                                         | Generates a random integer value within the default range: 0-99                                                            |
| `random_int(<LIMIT>)`                                                      | `random_int(10)`                        | Generates a random integer value within the custom range: 0-<LIMIT>                                                        |
| `random(<ITEMS>)`                                                          | `random(['value', 1, True])`            | Generates a random value from <ITEMS> provided                                                                             |
| `date()`                                                                   |                                         | Generates a today's date in format YYYY-MM-DD                                                                              |
| `date(<DAYS_DELTA>)`                                                       | `date(-1)`                              | Generates a date with customized days in format YYYY-MM-DD                                                                 |
| `date_time()`                                                              |                                         | Generates a current date time in format YYYY-MM-DD'T'HH:mm:SS                                                              |
| `date_time(<DAYS_DELTA>, <HOURS_DELTA>, <MINUTES_DELTA>, <SECONDS_DELTA>)` | `date(hours=5, minutes=-3)`             | Generates a date time with customized time in format YYYY-MM-DD'T'HH:mm:SS                                                 |
| `city()`                                                                   | `city()`                                | Generates a city name                                                                                                      |
| `city(<ALLOW_DUPLICATES>)`                                                 | `city(True)`                            | Generates a city name allowing for duplicates within a context                                                             |
| `city_of(<COUNTRY>)`                                                       | `city('GBR')`                           | Generates a city name of a specific country (name, iso3 or iso2)                                                           |
| `city_of(<COUNTRY>, <ALLOW_DUPLICATES>)`                                   | `city('United Kingdom', True)`          | Generates a city name of a specific country (name, iso3 or iso2) allowing for duplicates within a context                  |
| `country()`                                                                | `country()`                             | Generates a country name                                                                                                   |
| `country(<ALLOW_DUPLICATES>)`                                              | `country(True)`                         | Generates a country name allowing for duplicates within a context                                                          |
| `country(<ALLOW_DUPLICATES>, <COUNTRY>)`                                   | `country(False, 'GBR')`                 | Generates a country name of a specific country (iso3 / iso2) (`<ALLOW_DUPLICATES>` parameter is ignored)                   |
| `country_iso3()`                                                           | `country_iso3()`                        | Generates a country iso3 code                                                                                              |
| `country_iso3(<ALLOW_DUPLICATES>)`                                         | `country_iso3(True)`                    | Generates a country iso3 code allowing for duplicates within a context                                                     |
| `country_iso3(<ALLOW_DUPLICATES>, <COUNTRY>)`                              | `country_iso3(False, 'GB')`             | Generates a country iso3 code of a specific country (name / iso2) (`<ALLOW_DUPLICATES>` parameter is ignored)              |
| `country_iso2()`                                                           | `country_iso2()`                        | Generates a country iso2 code                                                                                              |
| `country_iso2(<ALLOW_DUPLICATES>)`                                         | `country_iso2(True)`                    | Generates a country iso2 code allowing for duplicates within a context                                                     |
| `country_iso2(<ALLOW_DUPLICATES>, <COUNTRY>)`                              | `country_iso2(False, 'United Kingdom')` | Generates a country iso2 code of a specific country (name / iso3) (`<ALLOW_DUPLICATES>` parameter is ignored)              |


## License

MIT


## Authors

- [@TomaszAniolowski](https://www.github.com/TomaszAniolowski)


## Acknowledgements

 - [SimpleMaps.com](https://simplemaps.com/data/world-cities) (Cities & countries data)

