python3 browser/src/browser.py http://localhost:8000/tests/lab7/singlelink.html
- The "LINK" text should be in blue
- The "Link" should be bold
- All of the text on the page should be large (40px font)

python3 browser/src/browser.py http://localhost:8000/tests/lab7/multi_line_paragraph.html
- The first line should have "Header" on a line all by itself
- The second paragraph should have multiple lines with spaces between the words
- All the text for the second paragraph should be lined up on the left side, inline with "Header"
- The third paragraph should have multiple lines and should be indented in from the left by 50px
- The fourth paragraph should have multiple lines and should be indented in from the right by 50px
- The fifth paragraph should have multiple lines and should be indented in from the right and left by 50px
- There should be an extra line between paragraphs but not between the header and first paragraph
- Should be able to scroll down and up with arrows and maintain relative positioning

python3 browser/src/browser.py http://localhost:8000/tests/lab7/page1to2.html
- Click the link to page 2, it should take you to page 2
- Click the link to page 1, it should take you back to page 1