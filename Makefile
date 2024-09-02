.PHONY: help
help:
	@echo "make help"
	@echo "make clean"
	@echo "make build"

.PHONY: clean
clean:
	@rm -rf api/

.PHONY: build
build: api/v1/airlines/iata/ api/v1/airlines/icao/
	@echo "Build completed"

api/v1/airlines/iata/: data.json
	python3 ./build.py generate --output=./api/v1 data.json airlines iata

api/v1/airlines/icao/: data.json
	python3 ./build.py generate --output=./api/v1 data.json airlines icao
