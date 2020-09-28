alias dev_environment="source ./.venv/bin/activate"
alias dev_clear_pycache_and_pyc="find . | grep -E \"(__pycache__|\.pyc|\.pyo$)\" | xargs rm -rf"
alias serve="python -m http.server 8000"
echo "python3 browser/src/browser.py https://browser.engineering/draft/html.html"
echo "pytest -sv browser/src/tests/test_parser.py"
echo "python -m http.server 8000"
echo "alias 'serve'"

dev_environment
