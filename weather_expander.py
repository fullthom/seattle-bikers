import csv

times = [str(t) + ":00:00 AM" for t in range(1, 12)]
times.extend([str(t) + ":00:00 PM" for t in range(1, 12)])


def expand(row):
    date = row[5].split(" ")[0]
    res = []
    for t in times:
        r = row.copy()
        r[5] = date + " " + t
        res.append(r)
    return res


def main():
    with open("weather.csv", "r") as f:
        with open("weather-expanded.csv", "w", newline="") as output_f:
            reader = csv.reader(f)
            writer = csv.writer(output_f)
            writer.writerow(next(reader))

            for row in reader:
                writer.writerows(expand(row))


if __name__ == "__main__":
    main()
