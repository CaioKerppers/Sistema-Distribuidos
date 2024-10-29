class ChunkServer:
    def __init__(self, chunk_id):
        self.chunk_id = chunk_id
        self.files = {}
        self.active = True

    def upload_file(self, file_id, file_data):
        if self.active:
            self.files[file_id] = file_data
            return f"File {file_id} stored in Chunk {self.chunk_id}."
        return f"Chunk {self.chunk_id} is inactive. File not stored."

    def download_file(self, file_id):
        if self.active:
            return self.files.get(file_id, None)
        return None

    def delete_file(self, file_id):
        if self.active and file_id in self.files:
            del self.files[file_id]
            return f"File {file_id} deleted from Chunk {self.chunk_id}."
        return None

    def update_file(self, file_id, new_data):
        if self.active and file_id in self.files:
            self.files[file_id] = new_data
            return f"File {file_id} updated in Chunk {self.chunk_id}."
        return None

    def view_files(self):
        if self.active:
            return self.files.keys()
        return None
