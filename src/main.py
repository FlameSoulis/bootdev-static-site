from markdown_to_html import *
import shutil 
import os
import sys

def main():
	basepath = "/"
	if len(sys.argv[1]) > 0:
		basepath = sys.argv[1]
	print("Clearing docs folder...")
	clear_docs_folder()
	print("Copying static files...")
	copy_static_files("static", "docs")
	# Generating time
	generate_pages_recursive("content", "template.html", "docs", basepath)
	#generate_page("content/index.md", "template.html", "docs/index.html")


def clear_docs_folder():
	if os.path.exists("docs"):
		shutil.rmtree("docs")

def copy_static_files(source, destination, folder=""):
	# Build a list of files and folders
	path_to_check = os.path.join(source, folder)
	desitnatin_path = os.path.join(destination, folder)
	files = os.listdir(path_to_check)
	# Legs go!
	print(f"Entering {path_to_check} > {desitnatin_path}...")
	if not os.path.exists(desitnatin_path):
		os.mkdir(desitnatin_path)
	for file in files:
		file_path = os.path.join(path_to_check, file)
		# Is this a folder?
		if not os.path.isfile(file_path):
			#Go go recursive!
			copy_static_files(path_to_check, desitnatin_path, file)
		else:
			# Just copy then!
			shutil.copy(file_path, desitnatin_path)

def generate_page(from_path, template_path, dest_path, basepath):
	# Sanity check time!
	if not os.path.exists(from_path):
		raise Exception(f"\"{from_path}\" does not exist!")
	if not os.path.isfile(from_path):
		raise Exception(f"\"{template_path}\" is not a file!")
	if not os.path.exists(template_path):
		raise Exception(f"\"{template_path}\" does not exist!")
	if not os.path.isfile(template_path):
		raise Exception(f"\"{template_path}\" is not a file!")
	# Announce things
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	# Open the file and read the juicy contents
	markdown_file = open(from_path)
	markdown_contents = markdown_file.read()
	markdown_file.close()
	# Do the same for the contents
	template_file = open(template_path)
	template_contents = template_file.read()
	template_file.close()
	# Process the markdown
	markdown_node = markdown_to_html_node(markdown_contents)
	markdown_html = markdown_node.to_html()
	# Get the title
	title = extract_title(markdown_contents)
	# Replace everything
	html_page = template_contents.replace("{{ Title }}", title)
	html_page = html_page.replace("{{ Content }}", markdown_html)
	html_page = html_page.replace("href=\"/", basepath)
	html_page = html_page.replace("src=\"/", basepath)
	# Does the desintation actually exist?
	dest_folder = os.path.dirname(dest_path)
	if not os.path.exists(dest_folder):
		os.makedirs(dest_folder)
	# Write it down, WRITE IT DOWN!
	newfile = open(dest_path, 'w')
	newfile.write(html_page)
	newfile.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
	files = os.listdir(dir_path_content)
	for file in files:
		file_path = os.path.join(dir_path_content, file)
		dest_file_path = os.path.join(dest_dir_path, file)
		if os.path.isfile(file_path):
			file_info = os.path.splitext(dest_file_path)
			if file_info[1] == ".md":
				generate_page(file_path, template_path, file_info[0]+".html", basepath)
		else:
			print(f"Entering {file_path}...")
			generate_pages_recursive(file_path, template_path, dest_file_path, basepath)


if __name__ == "__main__":
	main()