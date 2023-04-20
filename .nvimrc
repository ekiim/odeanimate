echo "Loading Project RC"
au BufWritePost *.py !pipenv run black %
