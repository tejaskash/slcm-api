# slcm-api
An API to get attendance and marks data from SLCM Portal at Manipal University.

## Request Format 
The server expects requests to be in the following format: 

``` JSON
{
  "request":
  {
    "credentials":
    {
      "username":"<USERNAME>",
      "password":"<PASSWORD>"
    },
    "type":"<TYPE>"
  }
}
```
Type can be set to ```ATTENDANCE``` , ```MARKS``` or ```ALL``` depending on what is required.
