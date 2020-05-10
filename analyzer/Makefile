RAW_DATA = data/raw
INTERIM_DATA = data/interim
PROCESSED_DATA = data/processed
MODELS = models

.PHONY: all fetch clean

all: fetch transform train

fetch: analyzer/data/fetch.py
	python -m analyzer.data.fetch ${ES_HOST} ${ES_INDEX}

transform: fetch
	python -m analyzer.data.transform

train: transform
	python -m analyzer.wv.train
	python -m analyzer.category.transform
	python -m analyzer.category.train

clean:
	rm $(RAW_DATA)/*
	rm $(INTERIM_DATA)/*
	rm $(PROCESSED_DATA)/*
	rm $(MODELS)/*
