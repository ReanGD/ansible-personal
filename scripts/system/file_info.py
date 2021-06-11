import os
from termcolor import colored


def get_dirs(base, names):
    return set([name for name in names if os.path.isdir(os.path.join(base, name))])


def get_files(base, names):
    return set([name for name in names if not os.path.isdir(os.path.join(base, name))])


def show_arr(key, text, diff, color):
    if len(diff) != 0:        
        print(colored(f'{text} ({key}):', color))
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

        show_arr(key, 'New dirs', actual_dirs - expected_dirs, 'yellow')
        show_arr(key, 'New files', actual_files - expected_files, 'yellow')
        show_arr(key, 'Removed dirs', expected_dirs - actual_dirs, 'red')
        show_arr(key, 'Removed files', expected_files - actual_files, 'red')


dir_map = {
    '~': [
        '.ansible',
        '.cache',
        'cloud',
        '.config',
        'doc',
        'downloads',
        '.local',
        '.pki',
        'projects',
        '.ssh',
        'tmp',
        '.vscode',
        '.dmrc',
        '.Xauthority',
        '.xsession-errors',
        '.xsession-errors.old',
    ],
    '~/.config': [
        'awesome',
        'bash',
        'bin',
        'Code',
        '.conan',
        'dconf',
        'Dharkael',        
        'doublecmd',
        'emacs',
        'enchant',
        'fd',
        'fontconfig',
        'git',
        'gnupg',
        'google-chrome',
        'gtk-3.0',
        'proxy',
        'pulse',
        'python',
        'redshift',
        'rofi',
        'session',
        'start',
        'sublime-text-3',
        'virt-viewer',
        'volumeicon',
        'yandex-disk',
        'yay',
        'zsh',
        'kxkbrc',
        'user-dirs.dirs',
        'user-dirs.locale',
    ],
}


if __name__ == '__main__':
    show_diff(dir_map)
