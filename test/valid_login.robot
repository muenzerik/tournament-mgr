*** Settings ***
Documentation       A test suite with a valid logins and registrations.
...
...                 This test has a workflow that is created using keywords in
...                 the imported resource file.
Resource            resource.robot
Library	            Process
Library             DatabaseLibrary
Suite Setup         SuiteSetup
Suite Teardown      SuiteTeardown


*** Keywords ***
SuiteSetup
    Start Process       flask   run   shell=yes   alias=flask
#    sleep               5s
    Initialize Database

SuiteTeardown
    Disconnect From Database
    Terminate Process   flask   True

Initialize Database
    Connect To Database	    psycopg2	maennerfestspiele	postgres	postgres	localhost	5432
    Execute Sql String      DELETE FROM Users;
    # pwd: 'mosbypwd'
    Execute Sql String      INSERT INTO Users ("UserName", "Surname", "FirstName", "Email", "Phone", "PasswordHash") VALUES ('ballot', 'Mosby', 'Ted', 'mosby@mosbiousdesigns.com', '0800-555-666', 'pbkdf2:sha256:150000$ycXECe8H$286f87814cb2c692c4b74c494b51a71081db7bee35ed9a6f95819d8dcf262c2b'); 

Valid Registration Template
    [Arguments]     ${user}     ${email}    ${passwd}
    Open Browser To Login Page
    Go To Register Page
    Input Username      ${user}
    Input Email         ${email}
    Input Password      ${passwd}
    Repeat Password     ${passwd}
    Submit Credentials
    Login Page Should Be Open
    [Teardown]    Close Browser


*** Test Cases ***
Valid Registration
    [Template]      Valid Registration Template
    user=barney     email=barney@gnb.com     passwd=theImpossimpible12345
    user=robin      email=sparkles@maplemalls.ca     passwd=anchorLady12345
    user=marshal    email=marshal@gnb.com    passwd=sasquatch12345
    user=lily       email=lily@mynursery.com     passwd=shoppingQueen12345

Valid Login
    Open Browser To Login Page
    Input Username    ballot
    Input Password    mosbypwd
    Submit Credentials
    Welcome Page Should Be Open
    [Teardown]    Close Browser