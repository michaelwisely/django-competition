Introduction
============

Django-competition is a reusable Django applicatian for creating
websites to manage competitions of different types. It was created to
help manage MegaminerAI: an artificial intelligence programming
competition held semesterly at Missouri S&T. Although it was created
to host a programming competition, it is intended to be flexible
enough to manoge other competitions as well.

It offers several nifty features:

* Creation of Competitions


Use Cases
=========

Competition
-----------

* Administrator

  * Create a competition
  * Delete a competition
  * Change competition options
    
    * Picture or poster
    * Scheduled start/end time
    * Cost per registered user
    * Minimum number of competitors per team
    * Maximum number of competitors per team

  * Create registration forms (to be answered by users prior to
    completing registration)

  * Start a competition
  * Stop a competition

  * Open registration and team activities
  * Close registration and team activities

* Competitor

  * Register for competition

    * Answer registration questions

  * Unregister for competition

Team
----

* Administrator or Organizer

  * Regulate team names and pictures

* Competitor

  * Invite other users to their team
  * Accept invitations to a team
  * Create a team
  * Leave a team

  * Change team details

    * Change team names
    * Change or add a picture

