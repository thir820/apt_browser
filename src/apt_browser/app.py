"""
Main application module of APT Browser.
"""
import logging

from . import __version__, init_logging, promo, log_exception


@log_exception(call_exit=True)
def main() -> None:
    """ Main entrypoint of APT Browser. """
    init_logging()

    logging.info('\n=========================\n'
                 'EBcL Root Generator %s\n'
                 '=========================\n', __version__)

    parser = argparse.ArgumentParser(
        description='Create the content of the root partiton as root.tar.')
    parser.add_argument('config_file', type=str,
                        help='Path to the YAML configuration file')
    parser.add_argument('output', type=str,
                        help='Path to the output directory')
    parser.add_argument('-n', '--no-config', action='store_true',
                        help='Skip the config script execution.')
    parser.add_argument('-s', '--sysroot', action='store_true',
                        help='Skip the config script execution.')

    args = parser.parse_args()

    logging.debug('Running root_generator with args %s', args)

    # Read configuration
    generator = RootGenerator(args.config_file, args.output, args.sysroot)

    # Create the root.tar
    image = None

    run_scripts = not bool(args.no_config)
    image = generator.create_root(run_scripts=run_scripts)

    generator.finalize()

    if image:
        print(f'Image was written to {image}.')
        promo()
    else:
        exit(1)


if __name__ == '__main__':
    main()
