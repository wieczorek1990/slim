
install:
	curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | /bin/bash
	brew install httpie poetry python3

run:
	./bin/run.fish

guard:
	./bin/guard.fish

query:
	./bin/query.fish
