def get_missing_dates(
    h5_dir_name: str,
    symbol: str,
    date_range: list[str],
) -> list[str]:
    h5_dir_name = f"data/market/h5/{symbol}"
    client = storage.Client()
    blobs = client.list_blobs("tabs-1", prefix=h5_dir_name)
    existing_dates = []
    for blob in blobs:
        blob_str = str(blob)
        stem = blob_str.split("/")[-1]
        if "-" not in stem:
            continue
        date = stem.split("-")[-1].split(".")[0]
        date_formatted = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        existing_dates.append(date_formatted)

    missing_dates = list(set(date_range) - set(existing_dates))
    print(
        f"Adding {symbol}-{len(missing_dates)}-{missing_dates} to the download queue..."
    )
    return missing_dates
