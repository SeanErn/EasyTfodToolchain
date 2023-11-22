from tflite_support import metadata as _metadata
import os
import argparse
import zipfile

DESCRIPTION = "Parses the metadata from a given tflite and exports it as JSON"
EXPORT_DIR = "./exportmeta"

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("filename",
        help="path to tflite file")
args = parser.parse_args()


if not os.path.isdir(EXPORT_DIR):
    print("Creating export directory...")
    os.mkdir(EXPORT_DIR)

try:
    displayer = _metadata.MetadataDisplayer.with_model_file(args.filename)
except:
    print("This model does not have any metadata. Is it a tensorflow v1 model?")
    exit(0)

export_json_file = os.path.join(EXPORT_DIR, args.filename+".json")
json_file = displayer.get_metadata_json()
# Optional: write out the metadata as a json file
with open(export_json_file, "w") as f:
  f.write(json_file)

with zipfile.ZipFile(args.filename, "r") as zip:
    zip.extractall(EXPORT_DIR)