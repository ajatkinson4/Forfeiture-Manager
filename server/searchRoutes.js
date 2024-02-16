const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');

router.use(express.static(path.join(__dirname, '..', 'client')));

router.get('/search', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'client', 'search.html'));
});

const STATES = {
    "ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ", "ARKANSAS": "AR", "CALIFORNIA": "CA",
    "COLORADO": "CO", "CONNECTICUT": "CT", "DELAWARE": "DE", "FLORIDA": "FL", "GEORGIA": "GA",
    "HAWAII": "HI", "IDAHO": "ID", "ILLINOIS": "IL", "INDIANA": "IN", "IOWA": "IA",
    "KANSAS": "KS", "KENTUCKY": "KY", "LOUISIANA": "LA", "MAINE": "ME", "MARYLAND": "MD",
    "MASSACHUSETTS": "MA", "MICHIGAN": "MI", "MINNESOTA": "MN", "MISSISSIPPI": "MS", "MISSOURI": "MO",
    "MONTANA": "MT", "NEBRASKA": "NE", "NEVADA": "NV", "NEW HAMPSHIRE": "NH", "NEW JERSEY": "NJ",
    "NEW MEXICO": "NM", "NEW YORK": "NY", "NORTH CAROLINA": "NC", "NORTH DAKOTA": "ND", "OHIO": "OH",
    "OKLAHOMA": "OK", "OREGON": "OR", "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI", "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD", "TENNESSEE": "TN", "TEXAS": "TX", "UTAH": "UT", "VERMONT": "VT",
    "VIRGINIA": "VA", "WASHINGTON": "WA", "WEST VIRGINIA": "WV", "WISCONSIN": "WI", "WYOMING": "WY"
};

function searchInJson(data, caseID, name, location) {
    let results = [];
    let searchLocation = location.toUpperCase();

    // Determine if the search term is a state (full name or abbreviation)
    let isStateSearch = Object.values(STATES).includes(searchLocation) || 
                        Object.keys(STATES).includes(searchLocation);

    for (let state in data) {
        let stateCases = data[state];

        stateCases.forEach(caseObj => {
            let caseKey = Object.keys(caseObj)[0];
            let caseInfo = caseObj[caseKey];
            
            // Split location into city and state parts
            let [caseCity, caseStateAbbreviation] = caseInfo.location.split(', ').map(part => part.trim().toUpperCase());
            let caseStateFullName = Object.keys(STATES).find(key => STATES[key] === caseStateAbbreviation);

            // Determine if there's a match for the location
            let locationMatch = false;
            if (location) {
                if (isStateSearch) {
                    // Compare state names/abbreviations
                    locationMatch = (searchLocation === caseStateAbbreviation) || (searchLocation === caseStateFullName);
                } else {
                    // City search
                    locationMatch = caseCity.includes(searchLocation);
                }
            }

            if ((!caseID || caseKey.includes(caseID)) &&
                (!name || caseInfo.name.toUpperCase().includes(name.toUpperCase())) &&
                (!location || locationMatch)) {
                    results.push({ caseID: caseKey, ...caseInfo });
            }
        });
    }

    return results;
}


router.post('/search', (req, res) => {
    const { agency, caseID, name, location } = req.body;

    let searchLocation = location.toUpperCase();
    if (STATES[searchLocation]) {
        searchLocation = STATES[searchLocation];
    }

    function searchFile(agency, callback) {
        const filePath = path.join(__dirname, 'database', 'agencyFiles', `${agency}.json`);
        fs.readFile(filePath, 'utf8', (err, jsonString) => {
            if (err) {
                // If the file does not exist, treat it as an empty search result
                if (err.code === 'ENOENT') {
                    return callback(null, []);
                } else {
                    return callback(err, null);
                }
            }
            try {
                const data = JSON.parse(jsonString);
                const results = searchInJson(data, caseID, name, searchLocation);
                callback(null, results);
            } catch (err) {
                callback(err, null);
            }
        });
    }

    if (agency) {
        // Search in the specified agency file
        searchFile(agency, (err, results) => {
            if (err) {
                console.log("Error:", err);
                return res.status(500).send('Error processing request');
            }
            res.json(results);
        });
    } 
    else {
        // Search across all agencies
        const agencies = [
            'ATF', 
            'DEA', 
            'FBI', 
            'IRS'
        ];
        let allResults = [];
        let completedRequests = 0;

        agencies.forEach(agency => {
            searchFile(agency, (err, results) => {
                completedRequests++;
                if (!err && results) {
                    allResults = allResults.concat(results);
                }
                // Once all files have been processed
                if (completedRequests === agencies.length) {
                    res.json(allResults);
                }
            });
        });
    }
});

module.exports = router;