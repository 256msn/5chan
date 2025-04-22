const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();
const port = 3000;

// Set up Multer storage engine to save files to the 'uploads' directory
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname)); // Generate unique filename
    }
});

const upload = multer({ storage: storage, limits: { fileSize: 5 * 1024 * 1024 } }); // Max 5MB file size

// Middleware to handle form data
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Serve static files from the "uploads" folder
app.use('/uploads', express.static('uploads'));

// Route for rendering the create thread form
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Route to handle thread creation (POST request) - image is now required
app.post('/create-thread', upload.single('file'), (req, res) => {
    const { title, content } = req.body;

    if (!req.file) {
        return res.status(400).send('Image is required.');
    }

    const imageUrl = `/uploads/${req.file.filename}`;

    // Store the thread (title, content, imageUrl) in the database
    console.log('Thread created:', { title, content, imageUrl });

    // Redirect to a page showing the newly created thread
    res.redirect('/');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});