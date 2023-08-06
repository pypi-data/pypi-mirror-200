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
    log to console  end

*** Keywords ***
High Level Keyword
    [Arguments]    ${arg}   ${arg2}
    middle  ${arg}
    middle  ${arg2}

middle
    [Arguments]    ${arg}
    low  ${arg}

low
    [Arguments]    ${arg}
    log to console  ${arg}