*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           Selenium2Library

*** Variables ***
${SERVER}         localhost:5000
${BROWSER}        Chrome
${DELAY}          0s
${VALID USER}     demo
${VALID PASSWORD}    mode
${LOGIN URL}      http://${SERVER}/login
${REGISTER URL}   http://${SERVER}/register
${WELCOME URL}    http://${SERVER}/index
${ERROR URL}      http://${SERVER}/error.html

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    Login Page

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Go To Register Page
    Go To    ${REGISTER URL}
    Register Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    username    ${username}

Input Email
    [Arguments]    ${email}
    Input Text    email    ${email}

Input Password
    [Arguments]    ${password}
    Input Text    password    ${password}

Repeat Password
    [Arguments]    ${password}
    Input Text    password2    ${password}

Submit Credentials
    Click Button    submit

Welcome Page Should Be Open
    Location Should Be    ${WELCOME URL}
    Title Should Be    Männerfestspiele

Register Page Should Be Open
    Location Should Be    ${REGISTER URL}
    Title Should Be    Register