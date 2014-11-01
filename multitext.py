#!/usr/bin/env python
# encoding: utf-8

from textmodel import TextModel

class MultiModel(TextModel):
	"""A TextModel containing multiple documents."""

	def __init__(self, name):
		super(name)
		docs = [] # List of documents contained
		doc_stems = {} # In how many documents have a given stem form appeared

	def __repr__(self):
		return super.__repr__() + "\n" + \
				"number of docs: " + str(doc_count)

	def addTextFromTextModel(self, tm):
		"""Adds a text model to the multimodel."""
		doc_count += 1

