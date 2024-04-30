from extractname import ExtractName

def main() -> None:
    extractname: ExtractName = ExtractName("list_users.csv")
    data: pd.DataFrame = extractname.get_users_list()
    extractname.show_data()


if __name__ == "__main__":
    main()
