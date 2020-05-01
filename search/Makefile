RAW_DATA = data/raw
PROCESSED_DATA = data/processed
MODELS = models

.PHONY: all fetch clean

all: fetch transform train

fetch: data/fetch.py
	python -m data.fetch ${ES_HOST} ${ES_INDEX}

transform: fetch
	python -m data.transform

train: transform
	python -m train

clean:
	rm $(RAW_DATA)/*
	rm $(PROCESSED_DATA)/*
	rm $(MODELS)/*
