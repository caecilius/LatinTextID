#!/usr/bin/env python
# encoding: utf-8

import subprocess
import string
import re
import json

# Helper functions
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

				# Parse the word into stem form and cache it in stemdict
				if w in stemdict:
					(stem, subst) = stemdict[w]
				else:
					stemdict[w] = self.stem(w)
					# Make manual adjustments for "sum" and "edo".
					if stemdict[w][0] == 'edo': stemdict[w] = ('sum', True)
					(stem, subst) = stemdict[w]

				# Increment appropriate counter and add the stem form if it is a substantive
				if stem == "" or stem.isspace():
					unknown_count += 1
				elif subst:
					subst_count += 1
					if stem not in self.stems: self.stems[stem] = 1
					else: self.stems[stem] += 1
				else:
					known_count += 1

			# Populate sentence length frequency dictionary
			if len(LoW) not in self.sentencelengths: self.sentencelengths[len(LoW)] = 1
			else: self.sentencelengths[len(LoW)] += 1

		# Print final statistics
		print "%d words processed in total, %d substantive, %d non-substantive, %d unknown" % \
				(known_count + subst_count + unknown_count, subst_count, known_count, unknown_count)

	def addTextFromFile(self, filename):
		"""Loads raw text from a file."""
		with open(filename) as fp:
			self.addTextFromString(fp.read().strip('\n'))

	def stem(self, wd):
		"""Parses the stem form of a Latin word.

		Returns a tuple (stem, is_subst), where is_subst is True iff stem is a substantive.

		IMPORTANT: This will only work if we have a copy of Whitaker's Words executable of the appropriate architecture!
		(A copy of OS X executable is included with the Python file.)"""

		def _is_subst(line):
			"""Tests whether a line of Whitaker's Words entry is a substantive.

			A substantive is defined as a Noun, a Verb (including a Participle), an Adjective, or an Adverb.

			Abbreviations are not considered substantives."""
			return (line.find(" N ")!=-1 or line.find(" V ")!=-1 or line.find(" ADJ ")!=-1\
					or line.find(" ADV ")!=-1) and not line.find(" abb. ")!=-1

		output = subprocess.check_output([r"./words/words", wd]) # Call Whitaker's Words, this works only on Unix-like OS
		out_lines = output.split('\n')
		best_level = 0 # 0=not found, 1=qualified, 2=unqualified
		for line in out_lines:
			if re.search(r"\[[A-Z]+\]", line): # Found a dict entry marker in the line (something like [XXXAX])
				if line.split(',')[0].split(' ')[0].strip() == "": # Not found
					pass
				if line.find("lesser") != -1 or \
						line.find("veryrare") != -1 or\
						line.find("uncommon") != -1: # Found a qualified (i.e., not ideal) result
					best_level = 1
					best = line.split(',')[0].split(' ')[0].strip()
					best_subst = _is_subst(line)
				else: # Found an unqualified result
					return (line.split(',')[0].split(' ')[0].strip(), _is_subst(line))
		if best_level == 0:
			return ("", False)
		else:
			return (best, best_subst)

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
					json.dumps(self.sentencelengths)) # Dump all data using json

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

