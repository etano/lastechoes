from urllib.request import urlopen

import bs4 as bs
import pandas as pd


def get_last_statement(uri):
    domain = r"http://www.tdcj.state.tx.us"
    if uri[0] == "/":
        url = domain + uri
    else:
        url = domain + r"/death_row/" + uri
    soup = bs.BeautifulSoup(urlopen(url).read(), "html.parser")
    ps = soup.find("div", {"id": "content_right"}).find_all("p")
    count = 0
    for p in ps:
        p = "".join(p.stripped_strings)
        if "Last Statement:" in p:
            break
        count += 1
    if count + 1 > len(ps) - 1:
        return None
    last_statement = " ".join("".join(ps[count + 1].stripped_strings).split())
    print(last_statement)
    return last_statement


def main():
    url = r"http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html"
    soup = bs.BeautifulSoup(urlopen(url).read(), "html.parser")
    parsed_table = soup.find_all("table")[0]
    data = [
        [td.a["href"] if td.find("a") else "".join(td.stripped_strings) for td in row.find_all("td")]
        for row in parsed_table.find_all("tr")
    ]
    headers = ["".join(th.stripped_strings) for th in parsed_table.find_all("th")]
    df = pd.DataFrame(data[1:], columns=headers)
    df.columns = pd.io.parsers.ParserBase({"names": df.columns})._maybe_dedup_names(df.columns)
    df["Last Statement"] = df["Link.1"].apply(get_last_statement)
    df = df[~df["Last Statement"].isnull()]
    print(df)
    df.to_csv("last.csv", encoding="utf-8")


if __name__ == "__main__":
    main()
