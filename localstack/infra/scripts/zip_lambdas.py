import os.path
import zipfile
from dotenv import load_dotenv

load_dotenv('lambda.env')


def zip_lambda(lambda_path: str, output_dir: str, output_name: str = None, depends_path: str = None):
    if not output_name:
        output_name = os.path.basename(lambda_path) + '.zip'
    output_path = os.path.join(output_dir, output_name)
    with zipfile.ZipFile(output_path, 'w') as zip_file:
        zip_file.write(lambda_path, arcname=os.path.basename(lambda_path))
        if depends_path:
            for path, subdirs, files in os.walk(depends_path):
                for name in files:
                    zip_file.write(os.path.join(path, name), os.path.relpath(os.path.join(path, name), depends_path))
        zip_file.close()


if __name__ == '__main__':
    lambda_source_path = os.getenv('LAMBDA_SOURCE_PATH')
    depends_path = os.getenv('LAMBDA_DEPENDS_PATH')
    lambda_zip_dir = os.getenv('LAMBDA_ZIP_FOLDER')

    for filename in os.listdir(lambda_source_path):
        if not os.path.isdir(os.path.join(lambda_source_path, filename)):
            zip_lambda(lambda_path=os.path.join(lambda_source_path, filename),
                       output_dir=lambda_zip_dir,
                       depends_path=depends_path)
