def calculate_user_discount(age: int, is_premium_member: bool, purchase_amount: float) -> float:
    """Calculate discount percentage based on user profile and purchase amount."""
    if age >= 65:
        base_discount = 0.15
    elif is_premium_member:
        base_discount = 0.10
    else:
        base_discount = 0.05
    return purchase_amount * base_discount



# This runs without error, even though types are completely wrong!
discount = calculate_user_discount(True, 1, 5)
print(discount)  # Output: 0.5 (True becomes 1, 1 is truthy, so 5 * 0.10)



# Multiply this by every data structure in your application, and you’ll spend more time # writing validation code than business logic.

# Pydantic solves this by combining three powerful concepts: type hints, runtime     alidation, and automatic serialization. Instead of manual checks, you define your data structure once using Python’s type annotation syntax, and Pydantic handles all the validation automatically:

# automatic serialization means you can easily convert your data structures to and from JSON, XML, YAML, and more.


from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    age: int
    email: EmailStr
    is_active: bool = True
    nickname: Optional[str] = None

# Pydantic automatically validates and converts data
user_data = {
    "age": "25",  # String gets converted to int
    "email": "john@example.com",
    "is_active": "true"  # String gets converted to bool
}

user = User(**user_data)
print(user.age)  # 25 (as integer)
print(user.model_dump())  # Clean dictionary output i.e {"age": 25, "email": "john@example.com", "is_active": True}


# Pydantic’s approach gives you several benefits. Performance is the first advantage you’ll notice — Pydantic’s core validation logic is written in Rust, making it faster than hand-written Python validation in most cases. Your application can process thousands of requests without validation becoming a bottleneck.

# Pydantic also allows integration with modern frameworks. FastAPI, one of Python’s fastest-growing web frameworks, uses Pydantic models to automatically generate API documentation, validate request bodies, and serialize responses. When you define a Pydantic model, you get OpenAPI schema generation for free:



from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

@app.post("/users/")
async def create_user(user: UserCreate):
    # FastAPI automatically validates the request body
    # and generates API docs from your Pydantic model
    return {"message": f"Created user {user.name}"}



# JSON schema generation happens automatically with every Pydantic model. This means your data structures become self-documenting, and you can generate clien libraries,validation rules for frontend applications, or database schemas from the same source of truth.





# Pydantic vs. Dataclasses vs. Marshmallow
# But when should you choose Pydantic over alternatives? If you're comparing Pydantic vs dataclasses, the decision comes down to validation needs. Pyhon's @dataclass is perfect for simple data containers where you trust the input, but Pydantic excels when you need validation, serialization, and integration with web framewrks:

# serialization means you can easily convert your data structures to and from JSON, XML, YAML, and more.

for dataclasses import dataclass
from pydantic import BaseModel

# Dataclass: fast, simple, no validation
@dataclass
class UserDataclass:
    name: str
    age: int


# Pydantic: validation, serialization, framework integration
class UserPydantic(BaseModel):
    name: str
    age: int

# Pydantic works best when you’re building APIs, processing external data, managing configuration, or any scenario where data validation failure should be caught early rather than causing mysterious bugs later. It converts runtime errors into clear, actionable validation messages that help both developers and users understand what went wrong.


"""
```bash
# Create and activate virtual environment (works in zsh and bash)
python -m venv pydantic_env
source pydantic_env/bin/activate  # On macOS/Linux
# pydantic_env\Scripts\activate  # On Windows

# pip install pydantic
# for email validation functionality
pip install "pydantic[email]"
"""

# The quotes around pydantic[email] are important in almost all terminals. Without them, you might see a "no matches found" error.
# Note: If you encounter ModuleNotFoundError: No module named 'pydantic', check these issues:
# Wrong Python environment: Make sure your virtual environment is activated
# Multiple Python versions: Verify you’re using the same Python version that installed Pydantic
# IDE configuration: Your code editor might be using a different Python interprete

# Critical naming warning: Never name your Python file pydantic.py. This creates a circular import that will break your code with confusing error messages. Python will try to import your file instead of the actual Pydantic library.


Your first Pydantic model
Let's build a simple user model to see Pydantic in action. Instead of starting with abstract examples, we'll solve a real problem: validating user registration data from a web form.

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    name: str
    email: EmailStr
    age: int
    is_active: bool = True
    created_at: datetime = None

# Test with clean data
clean_data = {
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 28
}
user = User(**clean_data)
print(f"User created: {user.name}, Age: {user.age}")
print(f"Model output: {user.model_dump()}")

# User created: Alice Johnson, Age: 28
# Model output: {'name': 'Alice Johnson', 'email': 'alice@example.com', 'age': 28, 'is_active': True, 'created_at': None}




# Let’s break down what’s happening in this model definition:
# Creating a Pydantic model: Your User class inherits from Basemodel, which gives it all of  Pydantic's validation and serialization capabilities. This inheritance turns regular python class into a data validation tool.

# Field definitions: Each line in the class defines a field with its expected type. The name: str syntax tells Pydantic that name should be a string, age: int means age should be an integer, and so on.
# EmailStr explained: EmailStr is a special Pydantic type that automatically validates email addresses. It comes from the pydantic[email] package you installed earlier and uses regular expressions to ensure the email format is valid. If someone passes "not-an-email", Pydantic will raise a validation error.
# Default values: Fields like is_active: bool = True have default values. If you don't provide these fields when creating a user, Pydantic uses the defaults. The = None for created_at makes this field optional.
# Model instantiation: When you call User(**clean_data), the ** unpacks your dictionary and passes each key-value pair as keyword arguments to the model constructor.
# Now let’s see Pydantic’s automatic type conversion in action:


# Messy data that still works
mess_data = {
    "name": "Bob Smith",
    "email": "bob@company.com",
    "age": "35",  # String instead of int
    "is_active": "true"  # String instead of bool
}

user = User(**mess_data)
print(f"Age type: {type(user.age)}")  # <class 'int'>
print(f"Is active type: {type(user.is_active)}")  # <class 'bool'>


# output
# Age type: <class 'int'>
# Is active type: <class 'bool'>

# As you can see, age and is_inactive fields are automatically converted to their proper formats through validation.
# When validation fails, Pydantic provides clear error messages:

from pydantic import ValidationError
try:
    invalid_user = User(
        name="",  # Empty string
        email="not-an-email",  # Invalid email
        age=-5  # Negative age
    )
except ValidationError as e:
    print(e)

# output
# 1 validation error for User
# email
#  value is not a valid email address: An email address must have an @-sign. [type=value_error, input_value='not-an-email', input_type=str]


# BaseModel vs. data classes
# Understanding when to use Pydantic's Basemodel versus Python's @dataclass helps you choose the right tool for each situation.

Python dataclasses are perfect for simple data containers where you control the input:

from dataclasses import dataclass
@dataclass
class ProductDataclass:
    name: str
    price: float 
    in_stock: bookl


# Fast, simple, but no validation
product = ProductionDataclass("Laptop", 999.99, True)

# This also works, even though types are wrong:
broken_product = ProductDataclass(123, "expensive", "maybe")




# Pydantic models add validation, serialization, and framework integration
from pydantic import BaseModel, Field

class ProductPydantic(BaseModel):
    name: str= Fiel(min_length)
    price: float=Field(gt=0)
    in_stock: bool

# Automatic validation prevents bad data
try:
    product = ProductPydantic(name="", price=10, in_stock="maybe")
    except ValidationError as e:
        print("Validation caught the errors!")
    

# Valid data works perfectly
good_product = ProductPydantic(
    name="Laptop",
    price="999.99",
    in_stock=True
)

# When to choose each approach:

# Use dataclasses for internal data structures, configuration objects, or when performance is critical and you trust your data sources
# Use Pydantic for API endpoints, user input, external data parsing, or when you need JSON serialization
# Pydantic adds some overhead compared to dataclasses, but this cost is usually negligible compared to the bugs it prevents and development time it saves. For web applications, the automatic integration with frameworks like FastAPI makes Pydantic the clear choice.

# The validation and serialization features become more valuable as your application grows. Starting with Pydantic models gives you a solid foundation that scales with your needs

# Building data models with Pydantic
# Now that you understand the basics, let's tackle the challenges you'll face when building production-ready applications.

# Field validation and constraints 
# Consider a product catalog API where price data comes from multiple vendors with different formatting standards. Some send prices as strings, others as floats, and  occassionally, someone needs a negative price that crashes your billing system.

# Pydantic's Field() function transforms basic type hints into sophisticated validation rules that protect your application: 

from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0, le=10000)
    description: optional[str] = Field(None, max_length=500)
    category: str = Field(..., pattern=r'^[A-Za-z\s]') # only letters and spaces
    stock_quantity: int = Field(ge=0) # greater than or equal to 0 
    is_available: bool = True

# This works - all constraints satisfied
valid_product = Product(
    name="Wireless Headphones",
    price="199.99", # String converted to Decimal
    description="High-quality wireless headphones",
    category="Electronics",
    stock_quantity=50
)

# This fails with clear error messages
try:
    invalid_product = Product(
        name="", # Too short
        price=-50, # Negative price
        category="Electronics123", # Contains numbers
        stock_quantity=-5 # Negative stock
    )
except ValidationError as e:
    print(f"Validation errors: {len(e.errors())} issues found")


#Each Field() parameter serves a specific purpose: min_length and max_length prevent database schema violations, gt and le create business logic boundaries, and pattern formatted data using regular expressions. The Field(...) syntax with ellipsis marks the required fields, while Field(None, ...) creates optional fields with validation rules.


# Type coercion vs strict validation
# By default, Pydantic converts compatible types rather than rejecting them outright. This flexibility works well for user input, but some scenarios demand exact type matching:

from pydantic immport BaseModel, Field, ValidationError

# Default: Lenient type coercion
class FlexibleOrder(BaseModel):
    order_id: int
    total_amount: float
    is_paid: bool

# These all work due to automatic conversion
flexible_order = FlexibleOrder(
    order_id="12345", # String to int
    total_amount="99.99", # String to float
    is_paid="true" # String to bool
)

# Strict validation when precision matters
class StrictOrder(BaseModel):
    model_config = {"str_strip_whitespace": True, "validate_assignment": True}
    
    order_id: int= Field(strict=True)
    total_amount: float=Field(strict=True)
    is_paid: bool=Field(strict=True)













