import express from "express";
import http from "http";
import { Server } from "socket.io";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

const io = new Server(server);
io.on("connection", (socket) => {
  console.log("A user connected");
  const chunks = [];

  socket.on("mediaChunk", (chunk) => {
    console.log("Received media chunk");
    chunks.push(Buffer.from(new Uint8Array(chunk)));
  });

  socket.on("mediaComplete", () => {
    console.log("Received complete media");
    const filePath = path.join(
      __dirname,
      `uploads/interview-${Date.now()}.mp4`
    );
    const buffer = Buffer.concat(chunks);
    fs.writeFile(filePath, buffer, (err) => {
      if (err) {
        console.error("Failed to save media file:", err);
        socket.emit("serverMessage", "Failed to save media file.");
      } else {
        console.log("Media file saved:", filePath);
        socket.emit(
          "serverMessage",
          "Media file received and saved successfully."
        );
      }
    });

    chunks.length = 0; // Clear the chunks array for the next recording
  });

  socket.on("disconnect", () => {
    console.log("User disconnected");
  });

  socket.on("error", (err) => {
    console.error("Socket error:", err);
  });

  socket.on("clientMessage", (message) => {
    console.log("Client message:", message);
  });
});

server.listen(3000, () => {
  console.log("Server is running on port 3000");
});
