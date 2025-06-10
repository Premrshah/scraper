from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def get_full_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="load", timeout=60000)
        page.wait_for_timeout(3000)  # wait to allow full page load
        html = page.content()
        browser.close()
        return html

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        html = get_full_html(url)
        return jsonify({"url": url, "html": html})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
