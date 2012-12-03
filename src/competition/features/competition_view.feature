Feature: Interacting with competition views

    Scenario: View competition list without logging in
        Given I am not logged in
        When I try to view a list of competitions
        Then I see the following 2 competitions:
          | name                      |
          | MegaMinerAI 10: Galapagos |
          | MegaMinerAI 9: Space      |

    Scenario: View competition list while logged in 
        Given I am logged in as alice, whose password is "123"
        When I try to view a list of competitions
        Then I see the following 2 competitions:
          | name                      |
          | MegaMinerAI 10: Galapagos |
          | MegaMinerAI 9: Space      |

    Scenario: View competition detail while logged in
        Given I am logged in as alice, whose password is "123"
        When I try to view details for Galapagos
        Then I see the following 1 competition:
          | name                      | pk                       |
          | MegaMinerAI 10: Galapagos | megaminerai-10-galapagos |





          
