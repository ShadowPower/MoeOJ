from celery import shared_task

import os, zipfile

@shared_task
def unzip(zip_path, out_path):
    os.removedirs(out_path)
    zip = zipfile.ZipFile(zip_path)
    zip.extractall(out_path)
    zip.close()
    return 'unzip: ' + zip_path + ' to: ' + out_path

@shared_task
def ping():
    return 'PONG'
