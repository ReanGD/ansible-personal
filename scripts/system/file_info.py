import os
from termcolor import colored


def get_dirs(base, names):
    return set([name for name in names if os.path.isdir(os.path.join(base, name))])


def get_files(base, names):
    return set([name for name in names if not os.path.isdir(os.path.join(base, name))])


def show_arr(text, diff, color):
    if len(diff) != 0:
        print(colored(text, color))
        for name in diff:
            print(colored(name, color))
        print()


def show_diff(dir_map):
    for key, expected_arr in dir_map.items():
        base = os.path.expanduser(key)

        expected_dirs = get_dirs(base, expected_arr)
        expected_files = get_files(base, expected_arr)

        actual_arr = os.listdir(base)
        actual_dirs =  get_dirs(base, actual_arr)
        actual_files = get_files(base, actual_arr)

        show_arr('New dirs:', actual_dirs - expected_dirs, 'yellow')
        show_arr('New files:', actual_files - expected_files, 'yellow')
        show_arr('Removed dirs:', expected_dirs - actual_dirs, 'red')
        show_arr('Removed files:', expected_files - actual_files, 'red')


dir_map = {
    '~': [
        '.ansible',
        '.cache',
        '.config',
        '.java',
        '.local',
        '.ssh',
        'cloud',
        'doc',
        'downloads',
        'projects',
        'tmp',
        '.dmrc',
        '.Xauthority',
        '.xprofile',
        '.xsession-errors',
        '.xsession-errors.old',
    ],
    '~/.config': [
        'awesome',
        'aurman',
        'bash',
        'bin',
        'doublecmd',
        'dconf',
        'emacs',
        'enchant',
        'fontconfig',
        'gconf',
        'google-chrome',
        'gtk-2.0',
        'gtk-3.0',
        'git',
        'gnupg',
        'menus',
        'mpv',
        'proxy',
        'pulse',
        'python',
        'sublime-text-3',
        'volumeicon',
        'yandex-disk',
        'zsh',
        'user-dirs.dirs',
        'user-dirs.locale',
        'QtProject.conf',
        '.Xresources',
    ],
}


if __name__ == '__main__':
    show_diff(dir_map)
