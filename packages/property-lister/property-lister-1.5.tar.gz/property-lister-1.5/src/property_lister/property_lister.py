#!/usr/bin/env python3

import datetime
import sys
import os
import sqlite3
import shutil
import re
import binascii
import biplist
import plistlib

start = datetime.datetime.now()

# -------------------------- INFO --------------------------

def basic():
	global proceed
	proceed = False
	print("Property Lister v1.5 ( github.com/ivan-sincek/property-lister )")
	print("")
	print("--- Extract from an SQLite unencrypted database file ---")
	print("Usage:   property-lister -db database -o out")
	print("Example: property-lister -db Cache.db -o results")
	print("")
	print("--- Extract from a property list file ---")
	print("Usage:   property-lister -pl property-list -o out")
	print("Example: property-lister -pl Info.plist    -o results")

def advanced():
	basic()
	print("")
	print("DESCRIPTION")
	print("    Extract and convert property list files")
	print("DATABASE")
	print("    SQLite unencrypted database file, or directory containing multiple files")
	print("    -db <database> - Cache.db | databases | etc.")
	print("PROPERTY LIST")
	print("    Property list file, or directory containing multiple files")
	print("    -pl <property-list> - Info.plist | plists | etc.")
	print("OUT")
	print("    Output directory")
	print("    All extracted propery list files will be saved in this directory")
	print("    -o <out> - results | etc.")

# ------------------- MISCELENIOUS BEGIN -------------------

def remove_directory(directory):
	removed = True
	try:
		if os.path.exists(directory):
			shutil.rmtree(directory)
	except Exception:
		removed = False
		print_error(("Cannot remove '{0}' related directories/subdirectories and/or files").format(directory))
	return removed

def create_directory(directory):
	created = True
	try:
		if not os.path.exists(directory):
			os.mkdir(directory)
	except Exception:
		created = False
		print_error(("Cannot create '{0}' related directories/subdirectories and/or files").format(directory))
	return created

def check_directory(directory):
	success = False
	overwrite = "yes"
	if os.path.exists(directory):
		print(("'{0}' directory already exists").format(directory))
		overwrite = input("Overwrite the output directory (yes): ").lower()
	if overwrite == "yes" and remove_directory(directory):
		success = create_directory(directory)
	return success

def check_directory_files(directory):
	tmp = []
	for file in os.listdir(directory):
		file = os.path.join(directory, file)
		if os.path.isfile(file) and os.access(file, os.R_OK) and os.stat(file).st_size > 0:
			tmp.append(file)
	return tmp

# -------------------- MISCELENIOUS END --------------------

# -------------------- VALIDATION BEGIN --------------------

# my own validation algorithm

proceed = True

def print_error(msg):
	print(("ERROR: {0}").format(msg))

def error(msg, help = False):
	global proceed
	proceed = False
	print_error(msg)
	if help:
		print("Use -h for basic and --help for advanced info")

args = {"database": None, "plist": None, "out": None}

# TO DO: Better site validation.
def validate(key, value):
	global args
	value = value.strip()
	if len(value) > 0:
		if key == "-db" and args["database"] is None:
			args["database"] = value
			if not os.path.exists(args["database"]):
				error("Directory containing files, or a single file does not exists")
			elif os.path.isdir(args["database"]):
				args["database"] = check_directory_files(args["database"])
				if not args["database"]:
					error("No valid files were found")
			else:
				if not os.access(args["database"], os.R_OK):
					error("File does not have read permission")
				elif not os.stat(args["database"]).st_size > 0:
					error("File is empty")
				else:
					args["database"] = [args["database"]]
		elif key == "-pl" and args["plist"] is None:
			args["plist"] = value
			if not os.path.exists(args["plist"]):
				error("Directory containing files, or a single file does not exists")
			elif os.path.isdir(args["plist"]):
				args["plist"] = check_directory_files(args["plist"])
				if not args["plist"]:
					error("No valid files were found")
			else:
				if not os.access(args["plist"], os.R_OK):
					error("File does not have read permission")
				elif not os.stat(args["plist"]).st_size > 0:
					error("File is empty")
				else:
					args["plist"] = [args["plist"]]
		elif key == "-o" and args["out"] is None:
			args["out"] = os.path.abspath(value)

def check(argc, args):
	count = 0
	for key in args:
		if args[key] is not None:
			count += 1
	return argc - count == argc / 2

# --------------------- VALIDATION END ---------------------

# ----------------- GLOBAL VARIABLES BEGIN -----------------

ext = {"blob": ".blob", "plist": ".plist", "xml": ".plist.xml"}

# ------------------ GLOBAL VARIABLES END ------------------

# ----------------------- TASK BEGIN -----------------------

def read_database(file):
	tmp = ""
	with sqlite3.connect(file) as db:
		tmp = ("").join(db.iterdump())
	db.close()
	return tmp

# database --> full path (external)
def dump(database, out):
	for db in database:
		count = 0
		data = read_database(db)
		if data:
			blobs = re.findall(r"(?<=,x')[\w\d]+", data, re.IGNORECASE)
			if blobs:
				for blob in blobs:
					count += 1
					open(os.path.join(out, os.path.basename(db) + "." + str(count) + ext["blob"]), "wb").write(binascii.unhexlify(blob))

# file --> full path (external/internal)
def extract(file, out, external = True):
	try:
		data = biplist.readPlist(file)
		if external:
			shutil.copyfile(file, os.path.join(out, os.path.basename(file)))
			file = os.path.join(out, os.path.basename(file))
		os.rename(file, file.rsplit(".", 1)[0] + ext["plist"])
		if isinstance(data, dict):
			count = 0
			for key in data:
				if isinstance(data[key], biplist.Data):
					string = biplist.readPlistFromString(data[key]) # NOTE: Extract a property list file from a property list file.
					if string:
						count += 1
						file = file.rsplit(".", 1)[0] + "." + str(count) + ext["plist"]
						biplist.writePlist(string, file)
						extract(file, out)
	except (biplist.InvalidPlistException, biplist.NotBinaryPlistException):
		pass

# file --> full path (internal)
def convert(file, out):
	try:
		data = None
		with open(file, "rb") as stream:
			data = plistlib.load(stream)
		stream.close()
		if data:
			open(file, "wb").write(plistlib.dumps(data, fmt = plistlib.FMT_XML))
			os.rename(file, file.rsplit(".", 1)[0] + ext["xml"])
	except (plistlib.InvalidFileException):
		pass

def main():
	argc = len(sys.argv) - 1

	if argc == 0:
		advanced()
	elif argc == 1:
		if sys.argv[1] == "-h":
			basic()
		elif sys.argv[1] == "--help":
			advanced()
		else:
			error("Incorrect usage", True)
	elif argc % 2 == 0 and argc <= len(args) * 2:
		for i in range(1, argc, 2):
			validate(sys.argv[i], sys.argv[i + 1])
		if not ((args["database"] and args["out"]) or (args["plist"] and args["out"])) or (args["database"] and args["plist"]) or not check(argc, args):
			error("Missing a mandatory option (-db, -o)")
			error("Missing a mandatory option (-pl, -o)", True)
	else:
		error("Incorrect usage", True)

	if proceed and check_directory(args["out"]):
		print("######################################################################")
		print("#                                                                    #")
		print("#                        Property Lister v1.5                        #")
		print("#                                   by Ivan Sincek                   #")
		print("#                                                                    #")
		print("# Extract and convert property list files.                           #")
		print("# GitHub repository at github.com/ivan-sincek/property-lister.       #")
		print("# Feel free to donate bitcoin at 1BrZM6T7G9RN8vbabnfXu4M6Lpgztq6Y14. #")
		print("#                                                                    #")
		print("######################################################################")
		if args["database"]:
			dump(args["database"], args["out"])
			for file in os.listdir(args["out"]):
				extract(os.path.join(args["out"], file), args["out"], False)
			for file in os.listdir(args["out"]):
				if file.lower().endswith(ext["plist"]):
					convert(os.path.join(args["out"], file), args["out"])
		elif args["plist"]:
			for file in args["plist"]:
				extract(file, args["out"])
			for file in os.listdir(args["out"]):
				if file.lower().endswith(ext["plist"]):
					convert(os.path.join(args["out"], file), args["out"])
		print(("Script has finished in {0}").format(datetime.datetime.now() - start))

if __name__ == "__main__":
	main()

# ------------------------ TASK END ------------------------
