import gc
import os


def rom_space():
    f_bsize, f_frsize, f_blocks, f_bfree, f_bavail, _, _, _, _, _ = os.statvfs('//')
    print('ROM: {0} Total {1} ({2:.2f}%) Free'.format(f_frsize * f_blocks, f_bsize * f_bfree,
                                                      ((f_bsize * f_bfree) / (f_frsize * f_blocks)) * 100))


def ram_space():
    free_ram = gc.mem_free()
    available_ram = gc.mem_alloc()
    total_ram = free_ram + available_ram
    percent_free = '{0:.2f}%'.format(free_ram / total_ram * 100)
    print('RAM: {0} Total {1} ({2}) Free'.format(total_ram, free_ram, percent_free))
