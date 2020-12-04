alias dev_environment="source ./.venv/bin/activate"
alias dev_clear_pycache_and_pyc="find . | grep -E \"(__pycache__|\.pyc|\.pyo$)\" | xargs rm -rf"
alias serve="python -m http.server 8000"
alias kill_port_8000="lsof -i tcp:8000 | grep Python | awk '{print \$2}' | xargs kill -9"
echo "python3 browser/src/browser.py https://browser.engineering/draft/html.html"
echo "pytest -sv browser/src/tests/test_parser.py"
echo "python -m http.server 8000"
echo "python3 server/server.py     // (port 8000)"
echo "alias 'serve'"
echo "alias 'kill_port_8000'"
echo "cd server; kill_port_8000 && python3 server.py"

dev_environment
