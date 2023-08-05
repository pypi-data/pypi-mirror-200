# Error Handler

## What is it?

This module implements a simple, yet flexible framework for handling errors and applying
specific strategies for various cases.  Basically, a function is decorated with the error-handler
wrapper, with or without a specific strategy, and exceptions (and for given strategies other error
situations) can be caught, processed and handled according to the needs of the user.

### Basic usage

The simplest use will be along these lines:

    @error_handler
    def error_prone_func(s: str):
        ...
        < code that might fail >
        ...
        return result

This will add a basic error handler to the function, using a default error strategy (just basic logging 
and re-raising the exception).  In this case, the handler will catch any exception from the function, 
handle it according to the default strategy, and finally raise the exception after processing.  Functionally, 
the benefits might be small, but it gives cleaner code with less nesting.

To supress the exception instead (not re-raised), this can be done by simply setting the re_raise property of the 
handler:

    @error_handler(re_raise=False)
    def function(x: int):
        < code >
        return something

This will still handle the exception using the supplied strategy, but it will not be raised further allowing normal 
execution to proceed (typically if the handled function is not really required, or if an error is not relevant to 
the process)

A slightly more involved example using retry:

    @error_handler(strategy=RetryStrategy())
    def my_function(x: int, y: int) -> int:
        < code >
        return something

This will use the RetryStrategy, providing basic retry functionality for the function.  Note that the function as a 
whole will be retried, with the same arguments.  If all retries fail, the strategy will return a result indicating 
failure, and the exception will be raised back to the caller.  

### Strategy configuration

The strategies may also be configured more specifically to each case, like this:

    @error_handler(strategy=RetryStrategy(retries=5, backoff=3, backoff_exponent=2, on_except_hook=do_on_exception_func))
    def my_function(x: int, y: int) -> int:
        < code >
        return something

This will override the default values of the strategy, using the user supplied values instead and in this case adding 
a function to be called on each exception when attempting the function/retry.  To reduce clutter and simplify reuse
these configurations can be instantiated outside the decorator and used where needed:

    # Set up different strategies for use in code

    # A simple retry strategy
    simple_retry = RetryStrategy(retries=5)
    
    # Retry with exponential backoff
    exp_backoff_retry = RetryStrategy(retries=10, backoff_exponent=2)
    
    # More complex handling of retries
    complex_retry = RetryStrategy(
        retries=4,
        backoff=5,
        backoff_exponent=2,
        handled_exceptions=(HTTPError, IOError, ConnectionError),
        on_except_hook=my_custom_error_logger,
        on_except_hook_args={"foo": "bar", "reference": transaction_id}
    )
 
    # -- End of strategies
   
    @error_handler(strategy=simple_retry)
    def func_a(n: int):
        <code>
        return something
    
    @error_handler(strategy=exp_backoff_retry)
    def func_b(n: int):
        <code>
        return something
    
    @error_handler(strategy=simple_retry)
    def func_c(n: int):
        <code>
        return something
    
    @error_handler(strategy=complex_retry)
    def func_d(n: int):
        <code>
        return something

### Advanced usage

It is also possible to use strategies for handling other types of errors than exceptions.  A typical
case here would be to handle the response of an http-request based on status code.  This is made trickier 
by the fact that you probably need to handle the result of the actual request, rather than the function 
containing the calling code.

As an example, we have the following function:

    def call_service():
        <prepare request>
        response = requests.post(url, headers=headers, data=request_data)
        <process response>
        return result

In this case, decorating the function with an error_handler wouldn't catch an error from the requests.post()
call, since the request would return a status code on the response object indicating the result, whether it is 
a success or otherwise (unless the call itself generated an exception i.e. unable to serialize the data element)
so the previous method of simply decorating like this wouldn't give us what we wanted:

    @error_handler(strategy=HttpErrorStrategy())
    def call_service():
        ...

It would catch exceptions from trying to process a missing body after an internal server error, but that might not be
what we want.  Let's say you know the service you are trying to call has availability issues, but getting the call 
across is critical to your application you might need to retry the call several times before allowing the program to
try to process the result of the request.  Simply setting the retry_on_error=True for the HttpErrorStrategy doesn't 
help, since we need to verify (handle) the response from the requests.post() directly.  This can be achieved through 
calling the decorator directly with the wrapped function call:

    response = error_handler(strategy=HttpErrorStrategy(retry_on_error=True))(requests.post)(url, headers=headers, data=request_data)

That looks complicated, but the structure is actually quite straight forward:

    decorator(<config parameters>)(<function to wrap>)(<function arguments>)

This syntax allows for using a handler directly on a single line of code if required.  Since decorators can be nested,
this allows for more complex handling, like in this imaginary example:

    # Set up default handling with additional custom logging on exception
    @error_handler(strategy=DefaultHandlingStrategy(on_except_hook=my_custom_logger))
    def example():
        <code>
    
        # Add retry for critical code
        @error_handler(strategy=RetryStrategy())
        def inner_function():
            <code>
            result = call_external_service()
            <code>
            # supress exceptions from non-critical component
            @error_handler(re_raise=False)(call_non_required_func)("data":result.content)
            return result
        
        <code>
        temp_result = inner_function()
        <process temp_result>
        return temp_result

This sets up a function with default error handling and custom logging, while enabling retry for an inner function (not
the whole function).  There is also a call to an unreliable dependency that can't be allowed to let the execution fail
(maybe has a tendency to cause timeouts due to long processing, but still get's the job done), so that call is wrapped
in an explicit local handler supressing any exceptions raised.

## Writing your own strategies

It is also pretty straight forward to write your own strategies for error handling to plug in:

Define a class that derives from ErrorHandlingStrategy:

    class MyErrorStrategy(ErrorHandlingStrategy)

Override the __init__(self) function:

    def __init__(
            self,
            *,
            handled_exceptions: Tuple[Type[Exception], ...] = None,
            on_except_hook: Callable[[Exception], None] = None,
            on_except_hook_args: Dict[str, Any] = None,
            # Arguments for custom handler goes here 
        ):
        super().__init__(handled_exceptions=handled_exceptions, on_except_hook=on_except_hook, on_except_hook_args=on_except_hook_args)
        
        # Custom init goes here

Implement the act-function in you strategy.  This is called by the error_handler to invoke the wrapped function:

    def act(self, func: Callable, *args, **kwargs) -> StrategyInvokeResult:
        # implementation goes here.

Add whatever logic/functionality you need to your strategy.

Once done, it can be injected into a handler easily:

    @error_handler(strategy=MyStrategy(<init params>))
    def func_to_be_handled():
        # do stuff

