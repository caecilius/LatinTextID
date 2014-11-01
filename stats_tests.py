#!/usr/bin/env python
# encoding: utf-8

import operator
from scipy import stats
from math import log

def get_top_stems(model, num):
	"""Gets the most frequently appeared stems in a text model and returns them as a list of tuples (stem, frequency).

	Keyword arguments:
	model -- The model to be used.
	num -- Number of results to be returned.
	"""
	sorted_stems = sorted(model.stems.iteritems(), key=operator.itemgetter(1), reverse=True)
	top_ten = list(sorted_stems)[:num]
	s = ""
	i = 1
	for line in top_ten:
		s += str(i) + "\t" + str(line[1]) + "\t\t" + line[0] + "\n"
		i += 1
	return s


def t_test_wlen(model1, model2):
	"""Performs Student's t-test on word lengths between model1 and model2.

	The test used is unpaired two-sample Student's t-test with Welch's correction.

	Returns a tuple (t_value, p_value)."""

	def _populate_sample_list(model):
		sample = []
		for (length, incidence) in model.wordlengths.iteritems():
			length = float(length)
			for i in range(incidence):
				sample.append(length)
		return sample

	sample1 = _populate_sample_list(model1)
	sample2 = _populate_sample_list(model2)
	result = stats.ttest_ind(sample1, sample2, equal_var=False)
	return result

def t_test_slen(model1, model2):
	"""Performs Student's t-test on sentence lengths between model1 and model2.

	The test used is unpaired two-sample Student's t-test with Welch's correction.

	Returns a tuple (t_value, p_value)."""

	def _populate_sent_sample_list(model):
		sample = []
		for (length, incidence) in model.sentencelengths.iteritems():
			length = float(length)
			for i in range(incidence):
				sample.append(length)
		return sample

	sample1 = _populate_sent_sample_list(model1)
	sample2 = _populate_sent_sample_list(model2)
	result = stats.ttest_ind(sample1, sample2, equal_var=False)
	return result

def bayes_score(model1, model2, ignore_common=False):
	"""Calculates the Naive Bayes score between model1 and model2."""
	COMMON_WORDS = ['sum', 'possum', 'eo', 'ad', 'non', 'ne', 'cum', 'res', 'omnis']
	model2_stems = sum(model2.stems.values())
	bayes_score = 0
	for stem in model1.stems.keys():
		if ignore_common and stem in COMMON_WORDS:
			continue
		if stem not in model2.stems:
			model2_prob = 1/float(model2_stems)
			bayes_score += log(model2_prob, 2) * model1.stems[stem]
		else:
			model2_prob = float(model2.stems[stem])/model2_stems
			bayes_score += log(model2_prob, 2) * model1.stems[stem]
	return bayes_score

