Artidem
===
[![Code Climate](https://codeclimate.com/github/sebastianbeyer/artidem/badges/gpa.svg)](https://codeclimate.com/github/sebastianbeyer/artidem)

Generate artificial Digital Elevation Models that appear somehow realistic using [Perlin noise](https://en.wikipedia.org/wiki/Perlin_noise)


![avalon](https://raw.githubusercontent.com/sebastianbeyer/artidem/master/avalon.jpg)

![foggymountains](https://raw.githubusercontent.com/sebastianbeyer/artidem/master/foggymountains.jpg)


## Usage
Generate DEM via
```
./artidem.py
```

and create plot
```
./plotdem.gmt <netcdffile>
```

Artidem also creates a lot more fields in the NetCDF, which are used in another project.
