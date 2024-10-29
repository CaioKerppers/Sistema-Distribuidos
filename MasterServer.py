from ChunkServer import ChunkServer

class MasterServer:
    def __init__(self):
        self.chunks = {i: ChunkServer(i) for i in range(1, 4)}
        self.file_index = {}
        self.activity_log = []

    def log_activity(self, message):
        self.activity_log.append(message)
        print(message)

    def view_logs(self):
        return "\n".join(self.activity_log) if self.activity_log else "No activity logs available."

    def activate_chunk(self, chunk_id):
        if chunk_id in self.chunks:
            self.chunks[chunk_id].active = True
            message = f"Chunk {chunk_id} activated."
            self.log_activity(message)
            return message
        return f"Chunk {chunk_id} not found."

    def deactivate_chunk(self, chunk_id):
        if chunk_id in self.chunks:
            self.chunks[chunk_id].active = False
            message = f"Chunk {chunk_id} deactivated."
            self.log_activity(message)
            return message
        return f"Chunk {chunk_id} not found."

    def distribute_file(self, file_id, file_data):
        parts = [file_data[i::3] for i in range(3)]
        self.file_index[file_id] = {}

        for i, part in enumerate(parts, 1):
            result = self.chunks[i].upload_file(file_id, part)
            self.log_activity(result)
            if "stored" in result:
                self.file_index[file_id][i] = part
        return f"File {file_id} uploaded."

    def download_file(self, file_id):
        file_parts = []
        for chunk_id, chunk in self.chunks.items():
            part = chunk.download_file(file_id)
            if part is not None:
                file_parts.append(part)
        if file_parts:
            content = ''.join(file_parts)
            self.log_activity(f"File {file_id} downloaded.")
            return f"Content of file {file_id}: {content}"
        return f"File {file_id} not found."

    def delete_file(self, file_id):
        deleted = False
        for chunk_id, chunk in self.chunks.items():
            result = chunk.delete_file(file_id)
            if result:
                deleted = True
        if deleted:
            self.file_index.pop(file_id, None)
            self.log_activity(f"File {file_id} deleted from system.")
            return f"File {file_id} deleted."
        return f"File {file_id} not found."

    def update_file(self, file_id, new_data):
        if file_id not in self.file_index:
            return f"File {file_id} not found."
        
        parts = [new_data[i::3] for i in range(3)]
        for i, part in enumerate(parts, 1):
            self.chunks[i].update_file(file_id, part)
        self.file_index[file_id] = {i + 1: parts[i] for i in range(3)}
        self.log_activity(f"File {file_id} updated with new content.")
        return f"File {file_id} updated."

    def view_files(self):
        files_status = []
        for chunk_id, chunk in self.chunks.items():
            files = chunk.view_files()
            if files is not None:
                files_status.append(f"Chunk {chunk_id}: {list(files)}")
            else:
                files_status.append(f"Chunk {chunk_id} is inactive or empty.")
        self.log_activity("Viewed files in each chunk.")
        return "\n".join(files_status)

    def handle_command(self, command):
        parts = command.strip().split()
        cmd = parts[0]

        if cmd == "upload":
            return self.distribute_file(parts[1], " ".join(parts[2:]))
        elif cmd == "download":
            return self.download_file(parts[1])
        elif cmd == "delete":
            return self.delete_file(parts[1])
        elif cmd == "update":
            return self.update_file(parts[1], " ".join(parts[2:]))
        elif cmd == "view":
            return self.view_files()
        elif cmd == "activate":
            return self.activate_chunk(int(parts[1]))
        elif cmd == "deactivate":
            return self.deactivate_chunk(int(parts[1]))
        elif cmd == "logs":
            return self.view_logs()
        else:
            return "Invalid command."
