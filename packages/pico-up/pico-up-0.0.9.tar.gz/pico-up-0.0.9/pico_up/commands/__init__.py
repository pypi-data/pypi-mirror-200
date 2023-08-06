from .command_free import CommandFree
from .command_init import CommandInit
from .command_image import CommandPrepareImage
from .command_push import CommandPush
from .command_version import CommandVersion
from .command_wipe import CommandWipe

available_commands = {
    'free': CommandFree,
    'init': CommandInit,
    'image': CommandPrepareImage,
    'push': CommandPush,
    'wipe': CommandWipe,
    'version': CommandVersion,
}
