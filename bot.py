from playwright.sync_api import sync_playwright

URL = "https://www.hctax.net/Property/listings/taxsalelisting"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle")

        # Try to click the disclaimer button
        for selector in ["text=I Agree", "text=Agree", "text=Accept"]:
            try:
                if page.locator(selector).first.is_visible(timeout=1500):
                    page.locator(selector).first.click()
                    break
            except:
                pass

        page.wait_for_timeout(2000)

        # Print the page title (simple proof it loaded)
        print("PAGE TITLE:", page.title())

        browser.close()

if __name__ == "__main__":
    main()
