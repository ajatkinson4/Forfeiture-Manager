//Modules
const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const searchRoutes = require('./searchRoutes');
const caseInfo = require('./caseInfo');
const victimLookup = require('./victimLookup');
const scheduler = require('./scheduler.js');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());
app.use(express.static('client'));

app.use(scheduler);
app.use(searchRoutes);
app.use(caseInfo);
app.use(victimLookup);

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'client', 'home.html'));
});

app.get('/records', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'client', 'records.html'));
});
    
app.get('/support', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'client', 'support.html'));
});

app.listen(PORT, async () => {
    console.log(`Server running on port ${PORT}`);
});

scheduler();