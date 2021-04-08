Feature: Delete an Event

User Story: As a user, I want to be able to delete events that are no longer needed so it doesn't clutter the rest.

Scenario: As a user, I want to be able to delete events that have been cancelled so it does not confuse myself and others. 

Given I am on the home page
When I click on "My Events" link
Then I should be on the "My Events" page
When I click on my event
Then I should see an option to delete event
When I click on delete event
Then I should no longer see the event on "My Events" page
