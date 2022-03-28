# Monster-Alert-Query-Mgmt
Create, check, and manage a large set of Monster Alert queries.

#### Description
Manage Quotes Cloud pre-written Monster database alerts for pipeline deployment alerting thresholds. Each pre-written query corresponds to a possible subscription to an alerting filter contingent upon the end-user's specified threshold paramters, values, and target AWS account.
 
#### Intended Audience
* Devops

#### Pre-requisites
* Python 3.7
* Monster Alerts API Keys for Quotes Cloud
* [apiChanges](./apiChanges.json) JSON file.

#### Usage

##### Help
`aws-alias-mgmt -h` [`--help`]

##### Parsed Variables
The script will dynamically parse and assign variables to dictionaires and lists, sourced in from a JSON file containing multiple objects. (see the [apiChanges](./apiChanges.json) file as an example). This source file is where the alerting configuration paramters are maintained to enable a more dynamic configuration base.

##### Options

* `-l` `--list`
  * List the API changes in JSON format
    * Taken only from the [parsed variables](#parsed-variables)
    * When enabled, other flags will be ignored

* `-c` COMMIT, `--commit` = COMMIT
  * [GET], [CHECK], [UPDATE], [POST], or [DELETE] the API changes
    * i.e., `-c GET` to list the active Monster database queries.

* `-t` TOKEN, `--token` = TOKEN
  * Monster Alert API Token
    * Required when the `-c (--commit)` flag is specified

##### Examples

  * List all active Monster alert Database queries
    * `alert-query-mgmt -c GET -t <API Token>`
  * Check all active Monster alert Database queries against the latest dictionary data
    * `alert-query-mgmt -c CHECK -t <API Token>`
  * Update all active Monster alert Database queries as per the latest dictionary data
    * `alert-query-mgmt -c UPDATE -t <API Token>`
      * Should be used over POST option
  * Post all active Monster alert Database queries as per the latest dictionary data
    * `alert-query-mgmt -c POST -t <API Token>`
      * Should only be used for initial query creation 
  * Delete all active Monster alert Database queries as per the latest dictionary data
    * `alert-query-mgmt -c DELETE -t <API Token>`
  * List the latest API data if changes were to be applied
    * `alert-query-mgmt -l`
