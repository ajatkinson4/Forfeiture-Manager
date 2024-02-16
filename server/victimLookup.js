const express = require('express');
const path = require('path');
const fs = require('fs');
const router = express.Router();

const caseInfo = require('./caseInfo');

router.use(caseInfo);

router.get('/contact/:caseID', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'client', 'contact.html'));
});

// Look up victim name within database and find previously fetched addresses

// Database Structure
// {
//     "name": {
//         location: "",
//         addresses: []
//     }
// }

// If name exists && location matches, then return all addresses for user to select from
// If name does not exists, call API to do a whitepages search 
    // Store founded addresses within database that corresponds to the victim's name & location

    

module.exports = router;