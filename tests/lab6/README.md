# Functional Tests

python3 browser/src/browser.py http://localhost:8000/tests/lab6/margin.html
- There should be a space after "Margin Bottom", a space to the left of "Margin Left", and a space above "Margin Top"
- "Margin Right should also have a space to the right of it. Resize the window to see this enforced.

python3 browser/src/browser.py http://localhost:8000/tests/lab6/externalstylesheet.html
- The small text should show up small (tag selector)
- The large text should show up large (class selector overridding tag selector)
- The regular text should show up regular (id selector overridding tag selector)
- All of the text should have left margin and top margin (shared css)

python3 browser/src/browser.py https://browser.engineering/draft/styles.html
- Sidenotes in the textbook should be in italics. This shows that an external stylesheet was loaded.