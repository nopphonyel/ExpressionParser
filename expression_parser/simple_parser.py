class SimpleParser:
    """
    The idea behind my design is...
    - if there is * and / operation, do it immediately
    - if there is -, convert the number into a negative number and put it in stack
    - if it just a number or known variable, just put into the stack
    - at the end I will sum all the number that remain in the stack

    - if there is parenthesis '(', ')'. Do the summation inside the parenthesis first
        - any rules above also apply inside the parenthesis

    At the end, the stack must have only 1 element left which is a result from the expression
    """

    def __init__(self):
        self.__stck = []
        self.__var_name = ""
        self.__known_var = {}

        self.__pending_op = None
        self.__pending_neg: bool = False

    def eval(self, expression: str):
        self.__stck_build(expression)
        return self.__stck.pop()

    def __stck_build(self, expression: str):
        # Try to get the value from the variable and eliminate all the operation except + and -
        # Also, do multiplication and dividing and
        for ch in expression:
            if ch == ' ':
                continue
            elif ch == '+':
                # DONE: parse var_name
                self.__parse_var_val()
                # If there is the pending op, run the pending_op_calc first
                self.__pending_op_calc()
                # DONE: we will assume that every element in stck will doing a summation on the end,
                # so we are not going to push the '+' to the stck
                # DONE: it can be waited for the ')' to trigger the calculation
            elif ch == '*' or ch == '/':
                # DONE: parse var_name first
                self.__parse_var_val()
                # DONE: If there is the pending op, run the calculation first
                self.__pending_op_calc()
                # DONE: pushing to the stack is required since there can be a stack of '*' and '('
                # for handle the case: 2*(3*(4*(3*4))) -> this also need some handle in pop_and_calc
                self.__stck.append(ch)
                # DONE: set as pending op
                self.__pending_op = ch
            elif ch == '-':
                # DONE: try to parse the variable if there is any variable in front of the '-'
                # for handle the case: 3-12
                self.__parse_var_val()
                # DONE: If found the '-' set pending_neg conversion to be true
                # The variable parser will handle the rest
                self.__pending_neg = True
            elif ch == '%':
                # DONE: parse var_name first
                self.__parse_var_val()
                # DONE: set pending_op
                self.__pending_op = ch
                # DONE: run pending_op_cal
                self.__pending_op_calc()
            elif ch == '(':
                # If there is a negative in front of '(', put it in stck. We will deal with it later in pop_and_calc
                if self.__pending_neg:
                    self.__stck.append('-')
                    self.__pending_neg = False
                # DONE: Push to stck and reset pending op
                self.__stck.append(ch)
                self.__pending_op = None
            elif ch == ')':
                # Also parse the value
                self.__parse_var_val()
                # DONE: In case that inside the parenthesis has a pending_op... calculate it first
                self.__pending_op_calc()
                # DONE: run pop_and_calc
                # pushing is not required: since the pop_and_calc require the first element that comes from pop to be
                # a number
                self.__pop_and_calc()
            else:
                # DONE: save it into the var_name for parse later
                self.__var_name = self.__var_name + ch
            # TODO: In the future release... support the power '^' operation

        # DONE: When it reaches the end of expression... this means that there is an operand that did not push to the
        # stck yet... push it!
        self.__parse_var_val()
        # Also run any pending_op
        self.__pending_op_calc()
        # DONE: So after elimination we need to do the calculation again till the stck has 1 element left
        # These process are same as the pop_and_calc function. So we can call pop_and_calc instead
        self.__pop_and_calc()

    def __pop_and_calc(self):
        # This will sum the number inside the '(' and ')'
        result = 0
        while len(self.__stck) > 0:
            # Pop first then check
            ch = self.__stck.pop()
            if ch == '(':  # This for handle the case that we want to do summarization inside the parenthesis '(', ')'
                break
            try:
                result = result + ch
            except TypeError:
                raise SyntaxError
        # DONE: When finish the summarization, put it back in top of stack
        self.__stck.append(result)
        # DONE: In the end, it needs to check that is there is any operand '*' or '/' with the '(...)'
        while len(self.__stck) > 1:
            # Saved the operation
            op = self.__stck[-2]
            # DONE: If there is no longer operation {*, /, -} in front of parenthesis then stop the loop
            if type(op) is float or op == '(':
                break
            # Now check the operation
            # DONE: Check negative in the front of '('
            elif op == '-':
                a = self.__stck.pop()
                self.__stck.pop()
                self.__stck.append(-a)
            # DONE: and then apply that calculation
            elif op == '*':
                b = self.__stck.pop()
                self.__stck.pop()
                a = self.__stck.pop()
                self.__stck.append(a * b)
            elif op == '/':
                b = self.__stck.pop()
                self.__stck.pop()
                a = self.__stck.pop()
                self.__stck.append(a / b)

    def __pending_op_calc(self):
        # DONE: if the pending calc is * and /, run the calc -> stck[-3] {* , /} stck[-1]
        if self.__pending_op is None:
            return
        elif self.__pending_op == '*':
            b = self.__stck.pop()
            self.__stck.pop()
            a = self.__stck.pop()
            self.__stck.append(a * b)
        elif self.__pending_op == '/':
            b = self.__stck.pop()
            self.__stck.pop()
            a = self.__stck.pop()
            self.__stck.append(a / b)
        # DONE: if the pending calc is %, run the calc -> stck[-1] * 0.01
        elif self.__pending_op == '%':
            a = self.__stck.pop()
            self.__stck.append(a * 0.01)
        else:
            raise SyntaxError("Unknown operation %s" % self.__pending_op)
        # DONE: at the end, set pending_op = None
        self.__pending_op = None

    # DONE
    def __parse_var_val(self):
        if len(self.__var_name) == 0:  # if there is no string in var_name, then there is nothing to do
            return
        try:
            if self.__var_name.count('.') == 0:
                parse_val = int(self.__var_name)
            else:
                parse_val = float(self.__var_name)
        except ValueError:
            try:
                parse_val = self.__known_var[self.__var_name]()
            except KeyError:
                raise KeyError("Variable %s is not known" % self.__var_name)
            except TypeError:
                parse_val = self.__known_var[self.__var_name]

            # DONE: If the pending_neg is True, then convert to negative value
        self.__stck.append(parse_val * -1 if self.__pending_neg else parse_val)
        # DONE: Reset var name, awaiting new one
        self.__var_name = ""
        # DONE: Also reset the pending_neg
        self.__pending_neg = False

    def define(self, var_name, callback):
        self.__known_var[var_name] = callback

    def view_stack(self):
        for item in self.__stck:
            print(item, end=', ')
