const express = require('express');
const path = require('path');
const fs = require('fs');
const router = express.Router();

router.get('/case/:caseID', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'client', 'caseInfo.html'));
});

// Reads the relevant JSON file based on the agency extracted from the caseID.
// Parses the file and searches for the case by the caseID.
// If found, sends the case details as a JSON response. If not found, sends a 404 error.
router.get('/:caseID', (req, res) => {
    const caseID = req.params.caseID;
    const agency = caseID.split('-')[1]; // Assuming the agency is part of the caseID
    const filePath = path.join(__dirname, 'database', 'agencyFiles', `${agency}.json`);

    fs.readFile(filePath, 'utf8', (err, jsonString) => {
        if (err) {
            console.error("Error reading file:", err);
            return res.status(500).send('Error reading database file');
        }

        try {
            const data = JSON.parse(jsonString);
            let foundCase = null;

            for (let state in data) {
                let stateCases = data[state];
                for (let caseObj of stateCases) {
                    if (caseObj[caseID]) {
                        foundCase = caseObj[caseID];
                        break;
                    }
                }
                if (foundCase) break;
            }

            if (foundCase) {
                return res.json(foundCase);
            } else {
                return res.status(404).send('Case not found');
            }
        } catch (err) {
            return res.status(500).send('Error parsing database file');
        }
    });
});

module.exports = router;