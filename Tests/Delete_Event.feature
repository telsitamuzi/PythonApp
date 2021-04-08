Feature: Delete event

User Story: As a user, I want to be able to delete events that are no longer needed so it doesn't clutter the rest.

Scenario: As a user, I want to be able to delete specific events
Given when I have an event selected
When I click the delete button
Then I should no longer see the event
And no one will be able to join the event
And the event will be gone
Then I can no longer see the event under the events list
