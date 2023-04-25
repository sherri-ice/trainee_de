import os.path
import zipfile
from dotenv import load_dotenv

load_dotenv('lambda.env')


class LargeLambdaException(Exception):
    pass


def _get_file_size_in_mb(filepath: str) -> float:
    """
    The _get_file_size_in_mb function returns the size of a file in megabytes.

    :param filepath: str: Specify the filepath of the file to be checked
    :return: The size of the file in megabytes
    """
    return os.stat(filepath).st_size / (1024 * 1024)


def zip_lambda(lambda_path: str, output_dir: str, output_name: str = None, depends_path: str = None):
    """
    The zip_lambda function creates a zip file of the lambda function at the given path and places it in the
    given directory. If no name is provided for the zip file, it will be named after its parent folder with
    .zip appended to it. Throws LargeLambdaException if the size of Lambda is too big.

    :param lambda_path: str: Specify the path to the lambda function
    :param output_dir: str: Specify the directory where the zip file will be created
    :param output_name: str: Specify the name of the output file
    :param depends_path: str: Specify the path to a directory that contains all the dependencies
    :return: A zip file of the lambda function and its dependencies
    """
    if not output_name:
        output_name = os.path.basename(lambda_path) + '.zip'
    output_path = os.path.join(output_dir, output_name)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(lambda_path, arcname=os.path.basename(lambda_path))
        if depends_path:
            for path, subdirs, files in os.walk(depends_path):
                for name in files:
                    zip_file.write(os.path.join(path, name), os.path.relpath(os.path.join(path, name), depends_path))
        zip_file.close()

        file_size = _get_file_size_in_mb(output_path)
        if file_size >= 50:
            raise LargeLambdaException(
                f"Lambda archive must be less than 50 MB. Lambda path: {output_path}, size: {file_size}")


if __name__ == '__main__':
    lambda_source_path = os.getenv('LAMBDA_SOURCE_PATH')
    depends_path = os.getenv('LAMBDA_DEPENDS_PATH')
    lambda_zip_dir = os.getenv('LAMBDA_ZIP_FOLDER')

    for filename in os.listdir(lambda_source_path):
        if not os.path.isdir(os.path.join(lambda_source_path, filename)):
            zip_lambda(lambda_path=os.path.join(lambda_source_path, filename),
                       output_dir=lambda_zip_dir,
                       depends_path=depends_path)
