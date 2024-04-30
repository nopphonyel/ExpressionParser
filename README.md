# ExpressionParser
This is my custom expression parser (as my programming exercise). The functions are similar to `eval()` in Python. 
In other words, this is my attempt to reimplement the `eval()` by myself without any guidance, so please don't expect 
the **blazingly fast** performance on this lib.

### Let's get started
1. Import my lib
    ```python
    from expression_parser import SimpleParser
    ```
2. Create the `SimpleParser` object
    ```python
    exprs = SimpleParser()
    ```
3. You can declare some custom variable inside your expression via callback function. **Lambda function** also accepted.
    ```python
    def randomness():
        r = random.randint(0, 10)
        return math.sin(r * 0.01 * math.pi)
    
    exprs.define(var_name="random_var", callback=randomness)
    exprs.define(var_name="กะเพราไข่ดาว", callback=lambda: 60)
    ```
4. Let's rock! with your expression
    ```python
    exprs.eval("(กะเพราไข่ดาว*2)*50/100")
    exprs.eval("random_var/(-2.00)")
    ```

### Differences from Python's `eval()`
1. I have introduced some weird operation which is `%`. This operation basically does the multiplication with `0.01`
   - For example: `50%` equals to `0.5`
2. Compared to Python's `eval()`, my expression parser has no `too many nested parentheses` error when the expression 
is too long
3. The callback function is tied to my method `define`. Therefore, it will perform the callback function multiple times
if you put your variable in more than one occurrence in your expression.
   - In my opinion, this is good in some cases, such as random variables..? maybe
   - Also, it may be worse in case that you let your callback perform some time-consuming task.
4. Of course, it is slower than Python's `eval()` in many cases.