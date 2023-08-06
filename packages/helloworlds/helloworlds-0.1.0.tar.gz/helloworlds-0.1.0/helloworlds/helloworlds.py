
class Hello:
    """
    Instantiate a multiplication operation.
    Numbers will be multiplied by the given multiplier.
    
    :param multiplier: The multiplier.
    :type multiplier: int
    """
    
    def sayhello(self):
        """
        Multiply a given number by the multiplier.
        
        :param number: The number to multiply.
        :type number: int
    
        :return: The result of the multiplication.
        :rtype: int
        """
        
        # Using NumPy .dot() to multiply the numbers
        print('Hello World...')


# Instantiate a Hello object
greetings = Hello()

# Call the  method
greetings.sayhello()