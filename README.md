# Django Air


## About

This is a service for managing airlines. 

<b>Stack:</b> Django, PostgreSQL, Ajax, jQuery, Bootstrap, Stripe.

Services has 2 interfaces:

### Passenger interface

Passengers are able to:

- search for the flights with destination and date;
- choose aditional options for their flight (such as lunch and luggage);
- get tickets on email;
- view tickets in personal cabinet;
- check-in with their tickets and choose additional luggage if needed;
- pay for tickets and additional luggage using personal cabinet;
- register for a flight;
- get refund in case their flight is canceled.

### Staff interface:

Staff can have 1 of 3 roles:

- check-in manager: confirms passenger check-ins;
- gate manager: confirms gate registration;
- supervisor: can do everything that check-in and gate managers do, and also edit their roless, create/cancel flights, add or remove flight options.
