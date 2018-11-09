from parser.parser import Parser


def main():
    parser = Parser()
    parser.start_trend("trend.csv")
    parser.start_custom("python", "custom.csv")


if __name__ == '__main__':
    main()
