import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: "http://localhost:8088", // Your client's URL
    methods: ["GET", "POST", "PUT", "PATCH", "OPTIONS"]
  }
});

const projectMembers = {}
const data = {}

io.on('connection', (socket) => {
  console.log('a user connected:', socket.id);

  // Handle text change event
  socket.on('text-change', (data) => {
    // Broadcast the text change to all other connected clients
    socket.broadcast.emit('text-change', data);
  });

  // Handle cursor move event
  socket.on('cursor-move', (data) => {
    // Broadcast the cursor move to all other connected clients
    socket.broadcast.emit('cursor-move', data);
    console.log(data)
    console.log('curso', socket.id);
  });

  socket.on('disconnect', () => {
    console.log('user disconnected:', socket.id);
    // Notify other clients that the user has disconnected
    socket.broadcast.emit('cursor-remove', { id: socket.id });
  });
});

const PORT = process.env.PORT || 3001;
httpServer.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
