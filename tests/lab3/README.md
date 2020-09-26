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