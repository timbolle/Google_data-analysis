import json, os
import argparse
import csv
import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="Le fichier MyActivity à parser")
    parser.add_argument("-o", "--output", required=True, help="Nom du fichier de sortie en csv")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        raise ValueError(f"{args.file} does not exist. Please put an existing json file")

    output_file = args.output.split(".")
    if output_file[-1] not in ["csv"]:
        raise ValueError(
            "A CSV file is waited as output. Please make sure that your output file has an .csv extension")
    if os.path.isfile(args.output):
        output_file[-2] += "_1"

        print(f"Warning!! {args.output} already exists. I will create {'.'.join(output_file)} instead!")

    output_file = '.'.join(output_file)

    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    header = ["number", "title", "date", "time", "response"]
    data_extracted = []
    for index, value in enumerate(data):
        time = datetime.datetime.strptime(value['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if "subtitles" in value.keys():
            response = " - ".join(map(lambda x: x["name"] if "name" in x.keys() else "", value["subtitles"]))
        else:
            response = ""

        data_extracted.append([index, value["title"], time.strftime("%Y.%m.%d"), time.strftime("%H:%M:%S"), response])

    with open(output_file, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow(header)
        writer.writerows(data_extracted)
