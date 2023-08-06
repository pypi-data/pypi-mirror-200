*** Settings ***


*** Test Cases ***
test1
    High Level Keyword    Next     High
    log to console  working
    @{list} =  Create List    hello    world
    Should Be Equal    ${list}[0]    Hallo
    Log     This is a log message
    Log To Console     Something here

test2
    log to console  another test case
    Fail    This is a failure
    log to console  end

test3
    Log To Console    start: 0 ,inc: 1 , end:10
    FOR    ${num}    IN RANGE    10
        Log To Console    ${num}
    END
    Log All


*** Keywords ***
High Level Keyword
    [Arguments]    ${arg}   ${arg2}
    middle  ${arg}
    middle  ${arg2}

middle
    [Arguments]    ${arg}
    low     ${arg}


low
    [Arguments]    ${arg}
    log       ${arg}


Log All
    [Arguments]    @{all}
    FOR    ${arg}    IN    @{all}
        Log To Console    ${arg}
    END