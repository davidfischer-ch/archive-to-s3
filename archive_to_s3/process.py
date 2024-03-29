#!/usr/bin/env python3

import argparse, logging, os, signal, socket, sys, yaml

import boto3, json_log_formatter
from pytoolbox import aws, crypto, filesystem
from pytoolbox.argparse import is_file, FullPaths

# https://docs.datadoghq.com/logs/processing/processors/#log-status-remapper
# https://en.wikipedia.org/wiki/Syslog#Severity_level
LEVEL_MAP = {
    'debug': 'debug',
    'info': 'info',
    'warning': 'warning',
    'error': 'error',
    'exception': 'error'
}


def main():
    signal.signal(signal.SIGINT, lambda *args: sys.exit(0))
    log = setup_log()

    parser = argparse.ArgumentParser(epilog='Archive stuff on S3.')
    parser.add_argument('--config', action=FullPaths, required=True, type=is_file)
    parser.add_argument('--simulate', action='store_true')
    parser.add_argument('--verbosity', choices=(0, 1, 2), default=0, type=int)
    args = parser.parse_args()

    def log_it(verbosity, level, message, **extra):
        if args.verbosity >= verbosity:
            extra['level'] = LEVEL_MAP[level]
            getattr(log, level)(message, extra=extra)

    s3 = boto3.client('s3')

    log_it(1, 'info', 'Process started')
    try:
        with open(args.config) as config_file:
            config = yaml.load(config_file)
        if config['enabled']:
            log_it(1, 'info', 'Its time to transfer!')
            if args.simulate:
                log_it(1, 'warning', 'Simulation mode enabled')

            for transfer in config['transfers']:
                name = transfer['name']
                log_it(1, 'info', 'Handling transfer', transfer=name)
                bucket = transfer['bucket']
                delete = transfer['delete']
                directory = transfer['directory']
                prefix = transfer['prefix'].format(host_fqdn=socket.getfqdn())

                processed_bytes = processed_count = skipped_bytes = skipped_count = 0

                for source_path in filesystem.find_recursive(
                    directory,
                    transfer['patterns'],
                    unix_wildcards=False
                ):
                    target_path = os.path.join(prefix, os.path.relpath(source_path, directory))
                    target_obj = aws.s3.load_object_meta(s3, bucket, target_path, fail=False)

                    with open(source_path, 'rb') as source_file:
                        # Retrieve metadata from source and target
                        source_size = filesystem.get_size(source_path)
                        target_size = None if target_obj is None else target_obj['ContentLength']
                        target_md5 = None if target_obj is None else target_obj['ETag'].strip('"')
                        source_md5 = crypto.checksum(
                            source_path,
                            is_path=True,
                            algorithm='md5',
                            chunk_size=1024 * 1024)
                        changed = source_md5 != target_md5

                        log_it(
                            2, 'info', 'File',
                            transfer=name,
                            changed=changed,
                            source_md5=source_md5,
                            source_path=source_path,
                            source_size=source_size,
                            target_md5=target_md5,
                            target_path=target_path,
                            target_size=target_size)

                        if changed:
                            processed_bytes += source_size
                            processed_count += 1
                        else:
                            skipped_bytes += source_size
                            skipped_count += 1

                        if not args.simulate:
                            aws.s3.write_object(s3, bucket, target_path, source_file)
                            if delete:
                                filesystem.remove(source_path)
                log_it(
                    1, 'info', 'Summary',
                    transfer=name,
                    processed_bytes=processed_bytes,
                    processed_count=processed_count,
                    skipped_bytes=skipped_bytes,
                    skipped_count=skipped_count)
        else:
            log.warning('Process is disabled')
    except Exception as e:
        log.exception(e)
    finally:
        log_it(1, 'info', 'Process ended')


def setup_log():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(json_log_formatter.JSONFormatter())
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


if __name__ == '__main__':
    main()
