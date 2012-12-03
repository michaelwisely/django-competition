Feature: Interacting with competition views

    Scenario: View team list while not logged in
        Given I am not logged in
        When I try to view a list of Galapagos teams
        Then I get redirected to "/accounts/login/"

    Scenario: View a team list while logged in
        Given I am logged in as alice, whose password is "123"
        When I try to view a list of Galapagos teams
        Then I see the following 2 teams:
          | name           |
          | Team Awesome   |
          | Galapagos Team |



          
