In a local terminal
run python3
import dukpy
dukpy.evaljs("1+1")
- This should return true and proves that dukpy is importable

python3 browser/src/browser.py http://localhost:8000/tests/lab9/simple_math_js.html
- Ensure that 32 is returned from the script

python3 browser/src/browser.py http://localhost:8000/tests/lab9/call_python.html
- This should print out "Hi from JS" to the logs

python3 browser/src/browser.py http://localhost:8000/tests/lab9/console_log.html
- This should print out "Hi from JS" to the logs

python3 browser/src/browser.py http://localhost:8000/tests/lab9/multiple_scripts.html
- This should log out "400"

python3 browser/src/browser.py http://localhost:8000/tests/lab9/js_page_crash.html
- This page should NOT crash. It's a js page error.
- The logs should say "Script js_page_crash.js crashed"

python3 browser/src/browser.py http://localhost:8000/tests/lab9/query_selector_all.html
- This should print out 3 lists of length 1, 1, and 3. (probably \[0], \[1], and \[0, 1, 2])

python3 browser/src/browser.py http://localhost:8000/tests/lab9/get_attribute.html
- This should print out "class_1", "class_2", "class_10", "class_20"
- It should print this out twice. Once for call_python and once for the Node.getAttribute wrapper

python3 browser/src/browser.py http://localhost:8000/tests/lab9/simple_character_count.html
- This should log "Input input3 has too much text."

python3 browser/src/browser.py http://localhost:8001/tests/lab9/inner_html.html
- Should display the text "This is my new bit of content!"
- The word "new" should be bold

run `python3 server.py` from "/server"
run `python3 browser/src/browser.py http://localhost:8000/`
- The guestbook should display with one entry
- Add a single short entry like "test". It should appear at the bottom on page refresh
- Add text to the textbox that is > 20 characters. A warning in red text should appear. The form should not be submitted when clicking the submit button.