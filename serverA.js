const http = require('http');

function createServer(port, serverName) {
    const server = http.createServer((req, res) => {
        const message = `Hello from ${serverName}, you requested: ${req.url}`;
        res.writeHead(200, { 
            'Content-Type': 'text/plain',
            'Content-Length': Buffer.byteLength(message)
        });
        res.end(message);
    });

    server.listen(port, () => {
        console.log(`${serverName} running on port ${port}`);
    });
}

// Create server instances
createServer(8881, 'ServerA-1');
createServer(8882, 'ServerA-2');
createServer(8883, 'ServerB-1');
createServer(8884, 'ServerB-2');