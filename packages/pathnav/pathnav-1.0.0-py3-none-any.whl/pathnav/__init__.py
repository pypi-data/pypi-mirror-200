import os
from . import errors
if __name__ != "__main__":
	class path():
		def __new__(self, path):
			if not os.path.isdir(path) and not os.path.isfile(path):
				raise errors.AbsentPathError
			self.isFile = os.path.isfile(path)
			path = path.replace("/", "\\")
			parts = path.split("\\")
			self.parts = [item for item in parts if item != ""]
			if self.isFile:
				self.file_name = self.parts[-1]
				del self.parts[-1]
				return filePath(self.parts, path, self.file_name)
			else:
				return dirPath(self.parts, path)

	class dirPath():
		def __init__(self, parts, path):
			self.parts = parts
			self.path = path
			self.dir_name = self.parts[-1]
			children = next(os.walk(self.path))
			self.child_dirs = children[1]
			self.child_files = children[2]
			self.dir_size = os.path.getsize(path)

		def up(self):
			if len(self.parts) < 2:
				raise errors.NoParentDirectoryError
			del self.parts[-1]
			self.path = "\\".join(self.parts)
			return dirPath(self.parts, self.path)

		def down(self, childDirectory):
			if not os.path.isdir(f"{self.path}\\{childDirectory}"):
				raise errors.AbsentChildDirectoryError
			self.path = f"{self.path}\\{childDirectory}"
			self.parts.append(childDirectory)
			return dirPath(self.parts, self.path)
		
		def get_file(self, file_name):
			file_path = f"{self.path}\\{file_name}"
			if not os.path.isfile(file_path):
				raise errors.AbsentFileError
			return filePath(self.parts, file_path, file_name)

	class filePath():
		def __init__(self, parts, path, file_name):
			self.parts = parts
			self.path = path
			self.file_name = file_name
			file_type = file_name.split(".")
			file_type.remove(self.file_name)
			file_type.insert(0, "")
			self.file_type = file_type[-1]
			self.parent_dir = dirPath(self.parts, "\\".join(self.parts))
