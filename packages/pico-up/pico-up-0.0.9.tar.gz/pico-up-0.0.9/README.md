# pico-up-and-running

A template repository with some scripts and shared functionality to get up and running with RaspberryPi Pico

## The `pico-up` command

```
python pico-up

free    show the current free ram and rom space, requires a soft-reset
init    initialise a python pico project in the current directory
image   prepare a 128x128 sprite image for use with the pico
push    push local application code to a connected pico
wipe    remove all files from a connected pico
version show the version of pico-up
```

## The `.pico-up.ini` file

This file configures how you want to communicate with and deploy code to the pico.

```ini
[device]
address = '/dev/ttyACM0' # The device id, name or path from mpremote devs

[push]
ignores = # File extensions to ignore when pushing files to the device
        .jpg
        .rgb332
        .bin

modules = # Code modules to push to the device in addition to your code
        pico_up_modules.msgpack_loads
```

For more information on available commands and their effects see [COMMANDS](docs/COMMANDS.md).
