# ComputerNetworking

## clientTerminal.py

### Chạy file

```bash
python clientTerminal.py
```

### Kết nối tới server

```bash
Server port: <serverPort>
Server IP: <serverIP>
Peer name: <peerName>
Peer port: <peerPort>
```

### Các lệnh

```bash
publish <lname> <fname>: Publish file lên Server.
files server: In ra terminal danh sách các file trên Server.
files local: In ra terminal danh sách các file trong máy người dùng, bao gồm các file đã publish và các file chưa publish.
delete <fname>: Xoá file tên <fname> khỏi server.
fetch <fname>: Tạo một bản copy của file <fname> về máy người dùng từ Server.
exit: Thoát khỏi Server.
```

## serverTerminal.py

### Chạy file

```bash
python serverTerminal.py
```

### Khởi động server

```bash
Server port: <serverPort>
Server IP: <serverIP>
```

### Các lệnh

```bash
ping <hostname>: Ping tới máy người dùng tên <hostname>.
discover <hostname>: In ra terminal danh sách các file được publish lên Server của <hostname>
list peer: In ra terminal danh sách các peer đang kết nối tới Server.
list file: In ra terminal danh sách các file được publish trên Server.
exit: Kết thúc Server.
```
