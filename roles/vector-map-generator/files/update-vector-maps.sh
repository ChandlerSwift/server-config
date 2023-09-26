#!/bin/sh

/usr/bin/java \
    -Xmx6g \
    -jar planetiler.jar \
    --download \
    --area=north-america \
    --mbtiles=north-america.mbtiles \
    --force

# from https://github.com/consbio/mbtileserver#reload-using-a-filesystem-watcher:
#
# > WARNING: do not generate tiles directly in the watched directories. Instead,
# > create them in separate directories and copy them into the watched
# > directories when complete.
mv north-america.mbtiles tilesets/north-america.mbtiles

# TODO: scp this to zirconium
