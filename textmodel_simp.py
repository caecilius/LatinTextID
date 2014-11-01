#!/usr/bin/env python
# encoding: utf-8

import string
import re
import json

class TextModel(object):
	"""A model for storing text identification data."""

	def __init__(self, name):
		"""Keyword arguments:
		name -- Identifying name of the text model.
		"""
		self.name = name
		self.words = {} # Dictionary of word frequencies
		self.wordlengths = {} # Dictionary of word length frequencies
		self.stems = {} # Dictionary of stem form frequencies
		self.sentencelengths = {} # Dictionary of sentence lenght frequencies

	def __repr__(self):
		s =  "text model name: " + self.name + "\n"
		s += "number of words: " + str(len(self.words)) + "\n"
		s += "number of word lengths: " + str(len(self.wordlengths)) + "\n"
		s += "number of sentence lengths: " + str(len(self.sentencelengths)) + "\n"
		s += "number of stems: " + str(len(self.stems)) + "\n"
		return s

	def addTextFromString(self, s):
		"""Loads a raw text from s and populates frequency dictionaries."""
		known_count = 0
		subst_count = 0
		unknown_count = 0

		stemdict = {}

		# Preprocess the text
		s = self.cleanText(s)

		lines = s.split('\n')
		for l in lines:
			if len(l) == 0: continue # Ignore empty lines
			LoW = l.split()

			for w in LoW:
				if w == "": continue # Ignore empty words
				w = w.lower()

				# Populate word and word length frequency dictionaries
				if w not in self.words: self.words[w] = 1
				else: self.words[w] += 1
				if len(w) not in self.wordlengths: self.wordlengths[len(w)] = 1
				else: self.wordlengths[len(w)] += 1

			# Populate sentence length frequency dictionary
			if len(LoW) not in self.sentencelengths: self.sentencelengths[len(LoW)] = 1
			else: self.sentencelengths[len(LoW)] += 1

	def addTextFromFile(self, filename):
		"""Loads raw text from a file."""
		with open(filename) as fp:
			self.addTextFromString(fp.read().strip('\n'))

	def stem(self, wd):
		# TODO
		pass

	def cleanText(self, s):
		"""Preprocesses text into an appropriate form."""

		def _sent_to_lines(sent):
			"""Converts a string of text to one sentence each line."""
			sent = re.sub(r"\n", " ", sent)
			return re.sub(r"(\.|\!|\?|--)+\s*", "\n", sent)

		def _strip_punct(sent):
			"""Strips away all punctuations from the text."""
			return sent.translate(string.maketrans("",""), string.punctuation)

		return _strip_punct(_sent_to_lines(s)).lower()

	def saveModelToFiles(self, filename=None):
		"""Saves the model to file.

		Keyword arguments:
		filename -- File name to be saved to. If empty, defaults to model name.
		"""
		if not filename: filename = self.name + ".model"
		with open(filename, "w") as fp:
			fp.write(json.dumps(self.words) + '\n' + \
					json.dumps(self.wordlengths) + '\n' + \
					json.dumps(self.stems) + '\n' + \
					json.dumps(self.sentencelengths)) # Dump all data using json, safer than print/eval

	def readModelFromFiles(self, filename=None):
		"""Loads the model from file.

		Keyword arguments:
		filename -- File name to be loaded from. If empty, defaults to model name.
		"""
		if not filename: filename = self.name + ".model"
		with open(filename, "r") as fp:
			lines = fp.readlines()
			(words, wordlengths, stems, sentencelengths) = lines
			# Load json data from file
			self.words = json.loads(words)
			self.wordlengths = json.loads(wordlengths)
			self.stems = json.loads(stems)
			self.sentencelengths = json.loads(sentencelengths)

