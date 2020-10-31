python3 browser/src/browser.py http://localhost:8000/tests/lab8/singleinput.html
- This should show a single input element in the top left of the page
- The input should start out empty
- Click on the element and type something, it should display in the input element
- A cursor should show in the element after clicking on it

python3 browser/src/browser.py http://localhost:8000/tests/lab8/inline_input.html
- The input element should show up inline with the rest of the text

python3 browser/src/browser.py http://localhost:8000/tests/lab8/placeholder_input.html
- The input element should come pre-populated with the value "Placeholder" in the gray box
- Click on the gray box and all the text should disappear
- Typing, the text should show up in the gray box

Start the web server `python3 server/src/server.py`
Open `http://localhost:8000/` in Chrome
- Make sure the web page pulls up and you can see the text "Guestbook"
- Try adding a couple entries and make sure it pulls up
- Open that URL using the toy browser and make sure it has the same functionality