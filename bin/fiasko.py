import os
import argparse

from fiasko_bro import validate
from fiasko_bro.configparser_helpers import extract_fiasko_config_from_cfg_file


def parse_args():
    parser = argparse.ArgumentParser(description='Static code analyser.')
    parser.add_argument('-p', '--path', type=str, default='.', dest='path')
    parser.add_argument('--config', type=str, default=None, dest='config_path')
    return parser.parse_args()


def main():
    args = parse_args()
    config_path = args.config_path or os.path.join(args.path, 'setup.cfg')
    updated_config = extract_fiasko_config_from_cfg_file(config_path)
    violations = validate(args.path, **updated_config)
    for violation_slug, violation_message in violations:
        print('%-40s\t%s' % (violation_slug, violation_message))
    print('=' * 50)
    print('Total %s violations' % len(violations))


if __name__ == '__main__':
    main()
