from playwright.sync_api import sync_playwright
import pandas as pd

URL = "https://www.hctax.net/Property/listings/taxsalelisting"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle")

        # Click disclaimer if it appears
        for selector in ["text=I Agree", "text=Agree", "text=Accept"]:
            try:
                if page.locator(selector).first.is_visible(timeout=1500):
                    page.locator(selector).first.click()
                    break
            except:
                pass

        page.wait_for_timeout(2000)

        # Grab the biggest table on the page
        tables = page.locator("table")
        if tables.count() == 0:
            print("No tables found after disclaimer.")
            browser.close()
            return

        best_table = None
        best_rows = 0
        for i in range(tables.count()):
            rc = tables.nth(i).locator("tr").count()
            if rc > best_rows:
                best_rows = rc
                best_table = tables.nth(i)

        # Extract headers + rows
        headers = []
        rows = []

        tr = best_table.locator("tr")
        for i in range(tr.count()):
            row = tr.nth(i)
            ths = row.locator("th")
            tds = row.locator("td")

            if ths.count() > 0 and not headers:
                headers = [ths.nth(j).inner_text().strip() for j in range(ths.count())]
                continue

            if tds.count() > 0:
                rows.append([tds.nth(j).inner_text().strip() for j in range(tds.count())])

        browser.close()

    df = pd.DataFrame(rows, columns=headers if headers else None)

    print("PAGE TITLE:", df.columns.tolist()[:5] if headers else "No headers detected")
    print("SCRAPED ROWS:", len(df))
    print(df.head(5).to_string(index=False))

if __name__ == "__main__":
    main()
