# Adding a new server operation

1. Create a file in the `operations` directory.
2. Implement the `BaseModule` abstract class, by supplying a list of supported message types and a method for processing messages.
3. Import the module above, and add an instance of it to the `modules` list below.
4. Include the Post and Response models to the union type so that our API can properly
   de/serialize the request and response.
