# pico-up-and-running

A template repository with some scripts and shared functionality to get up and running with RaspberryPi Pico

## The `pico-up` command

```
python pico-up

build   minify and attempt to compile pico application to bytecodes
init    initialise a python pico project in the current directory
image   prepare an image for use with the pico
push    push local application code to a connected pico
wipe    remove all files from a connected pico
version show the version of pico-up
```

### `init`

The init command will create the following directory structure.

```
.
├── app
│   └── __init__.py
├── .gitignore
├── .pico-up.ini
├── main.py
├── README.md
└── settings.py
```

#### Setting the right device

Use `mpremote connect list` to view a list of connected serial devices.

```
/dev/ttyACM0 xxxxxxxxxxxxx xxxx:cccc MicroPython Board in FS mode
/dev/ttyS1 None 0000:0000 None None
```

Choose the one in the list that says `MicroPython Board in FS mode`,
copying the first row of information, `/dev/ttyACM0` in this case.

Replace the line `address = 'CHANGE_ME'` with `address = '/dev/ttyACM0'` 
in the `.pico-up.ini` file.
