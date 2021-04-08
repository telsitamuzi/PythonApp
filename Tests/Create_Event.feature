Feature: Create an Event

User Story: As a user, I want to be able to create events so that I can organize them and see what needs to be done.

Scenario: As a user, I want to be able to navigate to the new event page and create an event
Given I am on the home page
When I click on the New Event tab
Then I should be on the Create an Event page
And I should see fields for event name, event description, and date
Given I have filled out these fields
When I click the submit button
Then I should be on the events page
And I should see the event I added
