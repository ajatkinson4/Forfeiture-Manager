const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');
const cron = require('node-cron');
const { exec } = require('child_process');

// Define the path to your Python script
const pythonScriptPath = '/database/dataScraper.py';

function startScheduler() {
    // Schedule the task to run every 24 hours (at midnight)
    cron.schedule('0 0 * * *', () => {
      console.log('Scheduled task running...');
  
      // Check the last execution timestamp (if available)
      let lastExecutionTimestamp = null;
      try {
        lastExecutionTimestamp = fs.readFileSync('lastExecution.txt', 'utf-8');
      } catch (error) {
        console.error('Error reading last execution timestamp:', error.message);
      }
  
      // Check if 24 hours have passed since the last execution
      const currentTime = Date.now();
      const twentyFourHoursInMillis = 24 * 60 * 60 * 1000; // 24 hours in milliseconds
  
      if (!lastExecutionTimestamp || currentTime - lastExecutionTimestamp >= twentyFourHoursInMillis) {
        // Execute the Python script
        exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
          if (error) {
            console.error('Error executing Python script:', error);
            return;
          }
  
          console.log('Python script output:', stdout);
  
          // Update the last execution timestamp
          fs.writeFileSync('lastExecution.txt', currentTime.toString(), 'utf-8');
        });
      } else {
        console.log('Not yet time for the next execution.');
      }
    });
  }
  
  module.exports = startScheduler;