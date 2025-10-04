
import asyncio
from pyppeteer import launch
import os

SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), 'snapshots')
SNAPSHOT_PATH = os.path.join(SNAPSHOT_DIR, '20min_snapshot.html')

async def main():
	# Fill the search form and submit
	search_success = False
	try:
		print("Waiting for search input...")
		await page.waitForSelector('form input[name="q"]', {'timeout': 7000})
		print("Simulating typing 'palestina'...")
		await page.click('form input[name="q"]')
		await page.focus('form input[name="q"]')
		for char in "palestina":
			await page.keyboard.type(char)
			await asyncio.sleep(0.1)
		print("Typing complete. Submitting form via JS...")
		await page.evaluate('''() => {
			var forms = document.querySelectorAll('form');
			for (var f of forms) {
				if (f.querySelector('input[name=\"q\"]')) {
					f.submit();
					break;
				}
			}
		}''')
		print("Submitted search for 'palestina'. Waiting for navigation...")
		await page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 15000})
		await asyncio.sleep(2)  # Extra wait for content
		search_success = True
	except Exception as e:
		print(f"Could not submit search form: {e}")

	# Take fourth DOM snapshot after search only if page is available
	if search_success:
		SNAPSHOT_PATH_4 = os.path.join(SNAPSHOT_DIR, '20min_snapshot_after_search.html')
		html4 = await page.content()
		with open(SNAPSHOT_PATH_4, 'w', encoding='utf-8') as f:
			f.write(html4)
		print(f"Fourth snapshot saved to {SNAPSHOT_PATH_4}")

		# Refined extraction: get only the text content of <span class='kilkaya-teaser-title'> inside <h2> for each article
		titles = await page.evaluate('''() => {
			return Array.from(document.querySelectorAll('article')).map(article => {
				const h2 = article.querySelector('h2');
				if (!h2) return null;
				const titleSpan = h2.querySelector('.kilkaya-teaser-title');
				return titleSpan ? titleSpan.textContent.trim() : null;
			}).filter(Boolean);
		}''')
		titles_path = os.path.join(SNAPSHOT_DIR, '20min_search_titles.txt')
		with open(titles_path, 'w', encoding='utf-8') as f:
			for line in titles:
				f.write(line + '\n')
		print(f"Extracted article titles saved to {titles_path}")
	browser = await launch(headless=False)
	page = await browser.newPage()
	await page.goto('https://www.20min.ch/', {'waitUntil': 'networkidle2'})
	# Take initial DOM snapshot (HTML content)
	html = await page.content()
	with open(SNAPSHOT_PATH, 'w', encoding='utf-8') as f:
		f.write(html)
	print(f"Initial snapshot saved to {SNAPSHOT_PATH}")

	# Click the 'Akzeptieren' button
	try:
		await page.waitForSelector('#onetrust-accept-btn-handler', {'timeout': 5000})
		await page.click('#onetrust-accept-btn-handler')
		print("Clicked 'Akzeptieren' button.")
		await asyncio.sleep(2)  # Wait for DOM to update
	except Exception as e:
		print(f"Could not click 'Akzeptieren' button: {e}")

	# Take second DOM snapshot after clicking
	SNAPSHOT_PATH_2 = os.path.join(SNAPSHOT_DIR, '20min_snapshot_after_accept.html')
	html2 = await page.content()
	with open(SNAPSHOT_PATH_2, 'w', encoding='utf-8') as f:
		f.write(html2)
	print(f"Second snapshot saved to {SNAPSHOT_PATH_2}")

	# Click the <a> tag with href='/discover'
	try:
		await page.waitForSelector('a[href="/discover"]', {'timeout': 5000})
		await page.click('a[href="/discover"]')
		print("Clicked <a href='/discover'>.")
		await page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 10000})
		await asyncio.sleep(2)  # Wait for navigation or DOM update
	except Exception as e:
		print(f"Could not click <a href='/discover'>: {e}")

	# Take third DOM snapshot after clicking
	SNAPSHOT_PATH_3 = os.path.join(SNAPSHOT_DIR, '20min_snapshot_after_discover.html')
	html3 = await page.content()
	with open(SNAPSHOT_PATH_3, 'w', encoding='utf-8') as f:
		f.write(html3)
	print(f"Third snapshot saved to {SNAPSHOT_PATH_3}")

	# Now interact with the search form (after discover)
	search_success = False
	try:
		print("Waiting for search input...")
		await page.waitForSelector('form input[name="q"]', {'timeout': 7000})
		print("Simulating typing 'palestina'...")
		await page.focus('form input[name="q"]')
		for char in "palestina":
			await page.keyboard.type(char)
			await asyncio.sleep(0.1)
		print("Typing complete. Submitting form via JS...")
		await page.evaluate('''() => {
			var forms = document.querySelectorAll('form');
			for (var f of forms) {
				if (f.querySelector('input[name=\"q\"]')) {
					f.submit();
					break;
				}
			}
		}''')
		print("Submitted search for 'palestina'. Waiting for navigation...")
		await page.waitForNavigation({'waitUntil': 'networkidle2', 'timeout': 15000})
		await asyncio.sleep(2)  # Extra wait for content
		search_success = True
	except Exception as e:
		print(f"Could not submit search form: {e}")

	# Take fourth DOM snapshot after search only if page is available
	if search_success:
		SNAPSHOT_PATH_4 = os.path.join(SNAPSHOT_DIR, '20min_snapshot_after_search.html')
		html4 = await page.content()
		with open(SNAPSHOT_PATH_4, 'w', encoding='utf-8') as f:
			f.write(html4)
		print(f"Fourth snapshot saved to {SNAPSHOT_PATH_4}")

	print("Browser will remain open. Press Ctrl+C to exit and close the browser.")
	try:
		while True:
			await asyncio.sleep(1)
	except KeyboardInterrupt:
		print("Ctrl+C detected. Closing browser...")
		await browser.close()

if __name__ == '__main__':
	asyncio.get_event_loop().run_until_complete(main())
