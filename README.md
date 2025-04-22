# 🔒 CYB5272 Final Project

## What is input validation?
Input validation is a part of Integrity in the CIA triad. It is used to ensure that the data entering a system meets the formatting requirements. Malicious actors can attack sites by SQL injection and XSS.

---

## Ways to analyze input validation

### 1. Analyze the client side by inspecting the HTML
- Look at the HTML code using dev tools to see how the input type of the username and password is set.
- The input type should be specified through a required pattern that eliminates the use of invalid characters or requests. 

### 2. Test input through black box testing
- Test black box input by entering certain edge cases which may go outside of the boundaries. 
- This can include:
    sql injection test, XSS test or directory traversal

### 3. Test the code for validation input
- Backend scripts written in javascript may include checks for email input methods. Invalid input is flagged. 
### 4. Analyze the database query
- Assess if the query in Sql prompts for raw user input

---
##Database assessment from the website's sql database




