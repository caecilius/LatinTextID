#!/usr/bin/env python
# encoding: utf-8

# Tkinter user interface
from Tkinter import *
import tkFileDialog
import tkSimpleDialog
import tkMessageBox

import const
from stats_tests import *
from textmodel import TextModel

# Create a window
root = Tk()
root.title("LatinTextID")
Label(root, text="LatinTextID v. " + const.VERSION).pack()

# Global variables
global_model = None
compare_model = None
multi_model = None
current_model_name = StringVar()
current_model_name.set("Current model: (none)")
compare_model_name = StringVar()
compare_model_name.set("Comparison model: (none)")
multi_model_name = StringVar()
multi_model_name.set("Multimodel: (not implemented)")

def generate(filename):
	"""Generates a text model from raw text and saves it to global_model."""
	global global_model, root
	model_name = filename.split("/")[-1].split("\\")[-1]
	model = TextModel(model_name)
	model.addTextFromFile("texts/" + filename + ".txt")
	print model
	model.saveModelToFiles("models/" + filename + ".model")
	tkMessageBox.showinfo("Success", "Success! Model saved to " + filename + ".model.")
	current_model_name.set("Current model: " + model_name)
	if global_model == None:
		enable_sample_1_buttons()
	global_model = model

def btngenerate():
	"""Queries user for file name and calls generate."""
	filename = tkFileDialog.askopenfilename(title="File name", filetypes=[("Text file (*.txt)",\
            "txt")], initialdir="./texts")
	filename = "".join(filename.split(".")[:-1])
	generate(filename)

def read(filename):
	"""Loads a text model from file and saves it to global_model."""
	global global_model
	model_name = filename.split("/")[-1].split("\\")[-1]
	model = TextModel(model_name)
	model.readModelFromFiles("models/" + filename + ".model")
	print model
	tkMessageBox.showinfo("Success", "Success! Model " + filename + ".model has been loaded.")
	current_model_name.set("Current model: " + model_name)
	if global_model == None:
		enable_sample_1_buttons()
	global_model = model

def btnread():
	"""Queries user for file name and calls read."""
        filename = tkFileDialog.askopenfilename(title="File name to load",\
                filetypes=[("Model file (*.model)", "model")],\
                initialdir="./models")
	filename = "".join(filename.split(".")[:-1])
	read(filename)

def summary():
	"""Shows summary (__repr__) of the current global_model."""
	global global_model
	tkMessageBox.showinfo("Summary",\
			"Summary of current model:\n" + \
			str(global_model))

def print_top_stems():
	"""Queries user for number and calls get_top_stems."""
	global global_model
	num = tkSimpleDialog.askinteger("Number", "Number of most common stems to print:")
	if num:
		tkMessageBox.showinfo("Summary",\
				"Top " + str(num) + " stems that appeared in the text:\n" + \
				get_top_stems(global_model, num))

def readcomp(filename):
	"""Loads a text model from file and saves it to compare_model."""
	global compare_model
	model_name = filename.split("/")[-1].split("\\")[-1]
	model = TextModel(model_name)
	model.readModelFromFiles("models/" + filename + ".model")
	tkMessageBox.showinfo("Success", "Success! Model " + filename + ".model has been loaded.")
	print model
	compare_model = model
	compare_model_name.set("Comparison model: " + model_name)
	enable_sample_2_buttons()

def btnreadcomp():
	"""Queries user for file name and calls readcomp."""
	filename = tkFileDialog.askopenfilename(title="File name to load", filetypes=\
                [("Model file (*.model)", "model")], initialdir="./models")
	filename = "".join(filename.split(".")[:-1])
	readcomp(filename)

def load_samples():
	"""Loads some sample files."""
	read("cic_milo")
	readcomp("caes_gal_1")

def print_t_test_wlen():
	"""Prints the result of the word length t-test."""
	tkMessageBox.showinfo("Result", "t-statistic: %.10f\np-value: %.10f" % t_test_wlen(global_model, compare_model))

def print_t_test_slen():
	"""Prints the result of the sentence length t-test."""
	tkMessageBox.showinfo("Result", "t-statistic: %.10f\np-value: %.10f" % t_test_slen(global_model, compare_model))

def print_bayes_score():
	"""Prints the result of Naive Bayes classifier."""
	tkMessageBox.showinfo("Result", "Naive Bayes score: %.6f" % bayes_score(global_model,\
		compare_model, ignore_common=True))

def create_multi():
	pass

def show_help():
	tkMessageBox.showinfo("Help",\
			"LatinTextID: A program to perform statistical inference on Latin text corpora.\n" +\
			"\n" +\
			"Three models can be loaded at once:\n" +\
			"Current model -- The main text model.\n" +\
			"Compare model -- The model to which the main text model is compared.\n" +\
			"Multimodel -- A model which supports multiple documents.")

# User interface elements
Button(root, text="Quick load samples", command=load_samples).pack(fill=BOTH, expand=1)
Label(root, textvariable=current_model_name).pack()
Button(root, text="Generate a new model", command=btngenerate).pack(fill=BOTH, expand=1)
Button(root, text="Load a model", command=btnread).pack(fill=BOTH, expand=1)
btnsummary = Button(root, text="Show model summary", command=summary, state=DISABLED)
btnsummary.pack(fill=BOTH, expand=1)
btntopten = Button(root, text="Get most common stems", command=print_top_stems, state=DISABLED)
btntopten.pack(fill=BOTH, expand=1)
Label(root, textvariable=compare_model_name).pack()
btnreadcomp = Button(root, text="Load a model to compare", command=btnreadcomp, state=DISABLED)
btnreadcomp.pack(fill=BOTH, expand=1)
btnttestwlen = Button(root, text="Unpaired t-test of word length", command=print_t_test_wlen, state=DISABLED)
btnttestwlen.pack(fill=BOTH, expand=1)
btnttestslen = Button(root, text="Unpaired t-test of sentence length", command=print_t_test_slen, state=DISABLED)
btnttestslen.pack(fill=BOTH, expand=1)
btnbayes = Button(root, text="Naive Bayes score of stem frequency", command=print_bayes_score, state=DISABLED)
btnbayes.pack(fill=BOTH, expand=1)
Label(root, textvariable=multi_model_name).pack()
btnnewmulti = Button(root, text="Create a new multimodel", command=create_multi, state=DISABLED)
btnnewmulti.pack(fill=BOTH, expand=1)
btnshowmulti = Button(root, text="Show multimodel summary", command=create_multi, state=DISABLED)
btnshowmulti.pack(fill=BOTH, expand=1)
btnaddtomulti = Button(root, text="Add current model to multimodel", command=create_multi, state=DISABLED)
btnaddtomulti.pack(fill=BOTH, expand=1)
btnbayestfidf = Button(root, text="Naive Bayes score with tf-idf corrections", command=create_multi, state=DISABLED)
btnbayestfidf.pack(fill=BOTH, expand=1)
Button(root, text="Help", command=show_help).pack(fill=BOTH, expand=1)
Button(root, text="Quit", command=quit).pack(fill=BOTH, expand=1)

# Functions to enable buttons after model has been loaded.
def enable_sample_1_buttons():
	btnsummary['state'] = 'normal'
	btntopten['state'] = 'normal'
	btnreadcomp['state'] = 'normal'

def enable_sample_2_buttons():
	btnttestwlen['state'] = 'normal'
	btnttestslen['state'] = 'normal'
	btnbayes['state'] = 'normal'

# Show window
root.mainloop()
