### The real guestbook should work
run `python3 server.py` at /server
run `python3 browser/src/browser.py http://localhost:8000/`
- You should be able to log in using username "bob" and password "123". (We go to a lot of work for secuity, but typing a long password is too much effort)
- You should be able to add an entry to the guestbook
- You should see a long random number that serves as a nonce

### Preventing Counterfeit Cookie 
run `python3 server.py` at /server
run `python3 browser/src/browser.py http://localhost:8000/`
- Manually add code to the browser setting the "username" cookie, you shouldn't be able to add guestbook entries
- Manually add code to the browser setting the "token" cookie, you shouldn't be able to add guestbook entries... unless you're REALLY lucky

### Same-Origin Policy
run `python3 server.py` at /server
run `python3 browser/src/browser.py http://localhost:8000/`
- Go to the guestbook and log in, you should see "Received cookie" with a token
run `http://localhost:9000/fakeform.html`
- Type the new url in the browser and go there. You should not see the token above in the request to the new server.

### Preventing XSS (Cross-Site Scripting)
run `python3 server.py` at /server
run `python3 -m http.server 9000` at /tests/lab11/evilserver
run `python3 browser/src/browser.py http://localhost:8000/`
- Log in and add a guestbook entry that has a full script tag in it. That script tag should not be run.
- The script tag should not display 

### Preventing CSRF (Cross-Site Request Forgery)
run `python3 server.py` at /server
run `python3 -m http.server 9000` at /tests/lab11/evilserver
run `python3 browser/src/browser.py http://localhost:9000/fakeform.html`
- You should see a single button that says "Click me", click that button
- You should see "Invalid nonce", this shows that nonces are used in the form for the real guestbook