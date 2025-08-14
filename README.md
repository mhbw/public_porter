# public_porter
public facing version of the ROAR Porter in order to make the resource available to others. 

The file shopify_to_discogs_drafts.py is the first step to having a working system to pull down the purchased SKUs and remove them from discogs inventory by setting them to draft. You can modify to hard delete as well. I'd recommend using draft both in case there is a return of the item, and as testing. 
next steps;

Prefect: 
  - create a prefect flow for this to run in the cloud

  - secure key storage: not sure how to safely do that in Prefect Cloud

  - webhooks: this can be set to run hourly as the current system does, but it would be best as a triggered event. not sure how to do those in Prefect yet.

Shopify:
  - currently this is pulling the open tickets, it should be updated to get the closed ones.

  - need to add some kind of logic then to check if the ticket has already been handled

  - webhooks: find what webhooks Shopify provides for purchases. 

