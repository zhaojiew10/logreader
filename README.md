# logreader

This is a simple HTTP server that serves files from a specified directory. It also supports automatic extraction of .gz files before serving them.

## Requirements
- Python 3.x

## usage

Clone or download the repository to your local machine.

Open a terminal or command prompt and navigate to the log directory.

Run the following command to start the HTTP server:

```python
cd /path/to/destination
python server.py
```

The server automatically extracts .gz files before serving them. If a requested file has a .gz extension, it will be extracted on-the-fly and sent to the client in its uncompressed form.

This server can use to read emr job log.

And if you use this server with s3 mount-poiny, you will get better experience.

The server will start running on http://localhost:8000 by default. You can change the port by modifying the PORT variable in the server.py file.

## docker

Please mount the log folder to container

```
docker run -it --rm -v /home/ec2-user/s3fs:/app/logreader -p 8000:8000 zhaojiew/logreader:latest 
```

