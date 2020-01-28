# Copyright Thomas Fuller 2020.
# Downloads CSV's as specified by the URLs in sources.csv

import csv
import urllib.request

headers = ["datetime", "cid", "direction", "mode", "count"]

pivoted_headers = [
    "datetime",
    "bicycle_north",
    "bicycle_south",
    "bicycle_east",
    "bicycle_west",
    "pedestrian_north",
    "pedestrian_south",
    "pedestrian_east",
    "pedestrian_west",
]

header_mapping = {
    "date": "datetime",
    "north": "bicycle_north",
    "south": "bicycle_south",
    "east": "bicycle_east",
    "west": "bicycle_west",
    "nb": "bicycle_north",
    "sb": "bicycle_south",
    "eb": "bicycle_east",
    "wb": "bicycle_west",
    "fremont_bridge_east_sidewalk": "bicycle_east",
    "fremont_bridge_west_sidewalk": "bicycle_west",
    "2100_7th_ave_display_total": "bicycle_west",
}


def fix_row_headers(row):
    # TODO: make this less awful
    res = {}
    i = 0
    for k, v in row.items():
        new_k = k.lower().replace(" ", "_").replace("bike", "bicycle").replace("ped", "pedestrian").strip()
        if new_k not in pivoted_headers and new_k in header_mapping:
            new_k = header_mapping[new_k]

        if new_k in pivoted_headers:
            res[new_k] = v

        i += 1
    return res


def main():
    with open("flattened.csv", "w") as output:
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        with open("sources.csv", "r") as sources:
            source_reader = csv.DictReader(sources)

            for source_row in source_reader:
                print("On cid = " + str(source_row["cid"]))
                reader = csv.DictReader(
                    urllib.request.urlopen(source_row["csv_url"]).read().decode("utf-8").splitlines())

                for row in reader:
                    row = fix_row_headers(row)

                    n = {
                        "datetime": row["datetime"],
                        "cid": source_row["cid"],
                    }

                    if len(row) == 2:
                        # The 7th ave counter is different.......
                        n["count"] = row["bicycle_west"]
                        n["mode"] = ""
                        n["direction"] = ""
                        writer.writerow(n)
                    else:
                        # Unpivot the columns into separate rows
                        for k, v in row.items():

                            if k != "datetime":
                                mode, direction = k.split("_")
                                n["mode"] = mode
                                n["direction"] = direction
                                n["count"] = v
                                writer.writerow(n)


if __name__ == "__main__":
    main()
