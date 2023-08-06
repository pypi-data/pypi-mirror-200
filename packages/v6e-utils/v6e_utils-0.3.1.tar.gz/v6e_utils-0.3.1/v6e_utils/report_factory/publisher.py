#  Copyright (c) 2023. ISTMO Center S.A.  All Rights Reserved
#

import logging
import os
import sys

import pysftp

logging.basicConfig(filename='sftp_publisher_operations.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ReportPublisher(object):
    server_url: str = None
    username: str = None
    password: str = None
    target_folder: str = None
    source_folder: str = None
    remove_source_file: bool = False
    remove_root_folder_if_empty: bool = False
    verbose: bool = True

    def __init__(self, params=None):
        if params is not None:
            self.server_url = params.get("server_url")
            self.username = params.get("username")
            self.password = params.get("password")
            self.source_folder = params.get("source_folder")
            self.target_folder = params.get("target_folder")
            self.remove_source_file = params.get("remove_source_file", self.remove_source_file)
            self.remove_root_folder_if_empty = params.get("remove_root_folder_if_empty",
                                                          self.remove_root_folder_if_empty)
            self.verbose = params.get("verbose", self.verbose)
            self.scan_and_upload_files()

    def scan_and_upload_files(self):
        try:
            with pysftp.Connection(host=self.server_url, username=self.username, password=self.password) as sftp:
                self.create_remote_folder(sftp, self.target_folder)
                for dir_path, _, filenames in os.walk(self.source_folder):
                    remote_root = os.path.join(self.target_folder, os.path.relpath(dir_path, self.source_folder))
                    self.create_remote_folder(sftp, remote_root)
                    for filename in filenames:
                        local_file = os.path.join(dir_path, filename)
                        remote_file = os.path.join(remote_root, filename)
                        if self.verbose:
                            print(f"Uploading...{local_file}")
                        sftp.put(local_file, remote_file, preserve_mtime=True)
                        logging.info(f'Uploaded {local_file} to {remote_file}')
                        if self.remove_source_file:
                            if self.verbose:
                                print(f"Deleting local file: {local_file}")
                            os.remove(local_file)
                            logging.info(f'Removed local file: {local_file}')
                        if len(os.listdir(dir_path)) == 0:
                            if self.remove_root_folder_if_empty:
                                if self.verbose:
                                    print(f"Removing empty local folder {dir_path}")
                                os.rmdir(dir_path)
                                logging.info(f'Removed local folder: {dir_path}')
        except Exception as ex:
            tb = sys.exc_info()[2]
            print(ex.with_traceback(tb))
            raise

    @staticmethod
    def create_remote_folder(sftp, folder):
        if not sftp.isdir(folder):
            sftp.mkdir(folder)
            logging.info(f'Created remote directory: {folder}')
