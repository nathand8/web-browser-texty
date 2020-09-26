### Unit tests

### Functional tests

Run `python3 browser/src/browser.py https://browser.engineering/draft/text.html`
- Check that the font matches what you expect (bold, italics, 16pt, Times)
- Press down to ensure you can still scroll down
- Resize the window to ensure words fill the page
- Examine the spacing between words, look for unnatural breaks or globs of text where there should be text

Run `python3 browser/src/browser.py http://www.simplehtmlguide.com/text.php`
- Check that the word "however" in the first part of the page is in italics

Run `python3 browser/src/browser.py http://www.cnn.com/US/OJ/`
- Yes, this is the CNN site for O.J. Simpson. I could only find <b> tags on old sites
- Scroll down to the bottom of the window. "More Simpson stories" should be bolded.

Spin up a Simple Web Server on port 8000 in the base of the repository using `python -m http.server 8000`
Run `python browser/src/browser.py http://localhost:8000/tests/lab3/bold_and_italics.html`
- Ensure that the bolded text is bolded, italics in italics, and Both italics and bolded works
- Ensure that the words "Normal" are back in the normal font
- Make sure all the text shares the same baseline

Run `python browser/src/browser.py http://localhost:8000/tests/lab3/font_sizes.html`
- Check that the small text is smaller
- Check that the big text is bigger
- Make sure all the text shares the same baseline

Run `python browser/src/browser.py http://localhost:8000/tests/lab3/newlines.html`
- Ensure that newlines are created for "br" and "p" tags