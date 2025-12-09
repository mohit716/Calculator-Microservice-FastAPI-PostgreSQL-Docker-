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

# Pydantic solves this by combining three powerful concepts: type hints, runtime     # validation, and automatic serialization. Instead of manual checks, you define your data structure once using Python’s type annotation syntax, and Pydantic handles all the validation automatically:



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
print(user.model_dump())  # Clean dictionary output


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


# JSON schema generation happens automatically with every Pydantic model. This means your data structures become self-documenting, and you can generate client libraries, validation rules for frontend applications, or database schemas from the same source of truth.


#Pydantic vs. Dataclasses vs. Marshmallow
#But when should you choose Pydantic over alternatives? If you’re comparing Pydantic vs dataclasses, the decision comes down to validation needs. Python’s @dataclass is perfect for simple data containers where you trust the input, but Pydantic excels when you need validation, serialization, and integration with web frameworks:



from dataclasses import dataclass
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


"""
```bash
# Create and activate virtual environment (works in zsh and bash)
python -m venv pydantic_env
source pydantic_env/bin/activate  # On macOS/Linux
# pydantic_env\Scripts\activate  # On Windows


pip install pydantic

# for email validation functionality
pip install "pydantic[email]"


"""

# The quotes around pydantic[email] are important in almost all terminals. Without them, you might see a "no matches found" error.

# Note: If you encounter ModuleNotFoundError: No module named 'pydantic', check these issues:

#Wrong Python environment: Make sure your virtual environment is activated
# Multiple Python versions: Verify you’re using the same Python version that installed Pydantic
#IDE configuration: Your code editor might be using a different Python interprete

#Critical naming warning: Never name your Python file pydantic.py. This creates a circular import that will break your code with confusing error messages. Python will try to import your file instead of the actual Pydantic library.



Your first Pydantic model
Let’s build a simple user model to see Pydantic in action. Instead of starting with abstract examples, we’ll solve a real problem: validating user registration data from a web form.

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

#User created: Alice Johnson, Age: 28
# Model output: {'name': 'Alice Johnson', 'email': 'alice@example.com', 'age': 28, 'is_active': True, 'created_at': None}


# Let’s break down what’s happening in this model definition:

#Creating a Pydantic model: Your User class inherits from BaseModel, which gives it all of Pydantic's validation and serialization capabilities. This inheritance turns a regular Python class into a data validation tool.
# Field definitions: Each line in the class defines a field with its expected type. The name: str syntax tells Pydantic that name should be a string, age: int means age should be an integer, and so on.
# EmailStr explained: EmailStr is a special Pydantic type that automatically validates email addresses. It comes from the pydantic[email] package you installed earlier and uses regular expressions to ensure the email format is valid. If someone passes "not-an-email", Pydantic will raise a validation error.
# Default values: Fields like is_active: bool = True have default values. If you don't provide these fields when creating a user, Pydantic uses the defaults. The = None for created_at makes this field optional.
# Model instantiation: When you call User(**clean_data), the ** unpacks your dictionary and passes each key-value pair as keyword arguments to the model constructor.
# Now let’s see Pydantic’s automatic type conversion in action:

# Messy data that still works
messy_data = {
   "name": "Bob Smith",
   "email": "bob@company.com",
   "age": "35",  # String instead of int
   "is_active": "true"  # String instead of bool
}

user = User(**messy_data)
print(f"Age type: {type(user.age)}")  # <class 'int'>
print(f"Is active type: {type(user.is_active)}")  # <class 'bool'>

# output
#Age type: <class 'int'>

#Is active type: <class 'bool'>



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
   # Shows exactly which fields failed and why
# 1 validation error for User
# email
#  value is not a valid email address: An email address must have an @-sign. [type=value_error, input_value='not-an-email', input_type=str]


# BaseModel vs. data classes
# Understanding when to use Pydantic’s BaseModel versus Python's @dataclass helps you choose the right tool for each situation.

# Python dataclasses are perfect for simple data containers where you control the input:

from dataclasses import dataclass

@dataclass
class ProductDataclass:
   name: str
   price: float
   in_stock: bool

# Fast, simple, but no validation
product = ProductDataclass("Laptop", 999.99, True)

# This also works, even though types are wrong:
broken_product = ProductDataclass(123, "expensive", "maybe")



# Pydantic models add validation, serialization, and framework integration:
from pydantic import BaseModel, Field

class ProductPydantic(BaseModel):
   name: str = Field(min_length=1)
   price: float = Field(gt=0)  # Must be greater than 0
   in_stock: bool

# Automatic validation prevents bad data
try:
   product = ProductPydantic(name="", price=-10, in_stock="maybe")
except ValidationError as e:
   print("Validation caught the errors!")

# Valid data works perfectly
good_product = ProductPydantic(
   name="Laptop",
   price="999.99",  # String converted to float
   in_stock=True
)


# When to choose each approach:

# Use dataclasses for internal data structures, configuration objects, or when performance is critical and you trust your data sources
# Use Pydantic for API endpoints, user input, external data parsing, or when you need JSON serialization
# Pydantic adds some overhead compared to dataclasses, but this cost is usually negligible compared to the bugs it prevents and the development time it saves. For web applications, the automatic integration with frameworks like FastAPI makes Pydantic the clear choice.

# The validation and serialization features become more valuable as your application grows. Starting with Pydantic models gives you a solid foundation that scales with your needs.

# Building Data Models With Pydantic
# Now that you understand the basics, let’s tackle the challenges you’ll face when building production-ready applications.

# Field validation and constraints
# Consider a product catalog API where price data comes from multiple vendors with different formatting standards. Some send prices as strings, others as floats, and occasionally, someone sends a negative price that crashes your billing system.

# Pydantic’s Field() function transforms basic type hints into sophisticated validation rules that protect your application:

from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class Product(BaseModel):
   name: str = Field(min_length=1, max_length=100)
   price: Decimal = Field(gt=0, le=10000)  # Greater than 0, less than or equal to 10,000
   description: Optional[str] = Field(None, max_length=500)
   category: str = Field(..., pattern=r'^[A-Za-z\s]+$')  # Only letters and spaces
   stock_quantity: int = Field(ge=0)  # Greater than or equal to 0
   is_available: bool = True

# This works - all constraints satisfied
valid_product = Product(
   name="Wireless Headphones",
   price="199.99",  # String converted to Decimal
   description="High-quality wireless headphones",
   category="Electronics",
   stock_quantity=50
)

# This fails with clear error messages
try:
   invalid_product = Product(
       name="",  # Too short
       price=-50,  # Negative price
       category="Electronics123",  # Contains numbers
       stock_quantity=-5  # Negative stock
   )
except ValidationError as e:
   print(f"Validation errors: {len(e.errors())} issues found")

#    Each Field() parameter serves a specific purpose: min_length and max_length prevent database schema violations, gt and le create business logic boundaries, and pattern validates formatted data using regular expressions. The Field(...) syntax with ellipsis marks the required fields, while Field(None, ...) creates optional fields with validation rules.


# Type coercion vs strict validation
#By default, Pydantic converts compatible types rather than rejecting them outright. This flexibility works well for user input, but some scenarios demand exact type matching:

from pydantic import BaseModel, Field, ValidationError

# Default: lenient type coercion
class FlexibleOrder(BaseModel):
   order_id: int
   total_amount: float
   is_paid: bool

# These all work due to automatic conversion
flexible_order = FlexibleOrder(
   order_id="12345",  # String to int
   total_amount="99.99",  # String to float
   is_paid="true"  # String to bool
)

# Strict validation when precision matters
class StrictOrder(BaseModel):
   model_config = {"str_strip_whitespace": True, "validate_assignment": True}
  
   order_id: int = Field(strict=True)
   total_amount: float = Field(strict=True)
   is_paid: bool = Field(strict=True)


#The model_config dictionary controls validation behavior across your entire model. The str_strip_whitespace option cleans string input automatically, while validate_assignment ensures field changes after model creation still trigger validation. Individual fields can override these settings with Field(strict=True) for situations requiring exact type matching, like financial calculations or scientific data.

#Nested models and complex data
#real applications handle complex, interconnected data structures. An e-commerce order contains customer information, shipping addresses, and multiple product items ,  each requiring its own validation:


from typing import List
from datetime import datetime

class Address(BaseModel):
   street: str = Field(min_length=5)
   city: str = Field(min_length=2)
   postal_code: str = Field(pattern=r'^\d{5}(-\d{4})?$')
   country: str = "USA"

class Customer(BaseModel):
   name: str = Field(min_length=1)
   email: EmailStr
   shipping_address: Address
   billing_address: Optional[Address] = None

class OrderItem(BaseModel):
   product_id: int = Field(gt=0)
   quantity: int = Field(gt=0, le=100)
   unit_price: Decimal = Field(gt=0)

class Order(BaseModel):
   order_id: str = Field(pattern=r'^ORD-\d{6}$')
   customer: Customer
   items: List[OrderItem] = Field(min_items=1)
   order_date: datetime = Field(default_factory=datetime.now)

# Complex nested data validation
order_data = {
   "order_id": "ORD-123456",
   "customer": {
       "name": "John Doe",
       "email": "john@example.com",
       "shipping_address": {
           "street": "123 Main Street",
           "city": "Anytown",
           "postal_code": "12345"
       }
   },
   "items": [
       {"product_id": 1, "quantity": 2, "unit_price": "29.99"},
       {"product_id": 2, "quantity": 1, "unit_price": "149.99"}
   ]
}

order = Order(**order_data)
print(f"Order validated with {len(order.items)} items")


#Optional fields and None handling
#Different operations need different data requirements. User creation demands complete information, while updates should accept partial changes:


from typing import Optional

class UserCreate(BaseModel):
   name: str = Field(min_length=1)
   email: EmailStr
   age: int = Field(ge=13, le=120)
   phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')

class UserUpdate(BaseModel):
   name: Optional[str] = Field(None, min_length=1)
   email: Optional[EmailStr] = None
   age: Optional[int] = Field(None, ge=13, le=120)
   phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')

# PATCH request with partial data
update_data = {"name": "Jane Smith", "age": 30}
user_update = UserUpdate(**update_data)

# Serialize only provided fields
patch_data = user_update.model_dump(exclude_none=True)
print(f"Fields to update: {list(patch_data.keys())}")


Serialization converts Pydantic objects back into dictionaries or JSON strings for storage or transmission. The model_dump() method handles this conversion, with exclude_none=True removing unprovided fields. This pattern works perfectly for PATCH requests where clients send only the fields they want to change, preventing accidental data overwrites in your database.

This foundation prepares you for the next challenge: implementing custom validation logic that captures your application’s unique business rules.

Custom Validation and Real-World Integration
Building production applications means handling data that doesn’t fit standard type-checking patterns.

Consider a user registration form where password requirements vary based on subscription plans, or an API that receives address data from multiple countries with different postal code formats. These scenarios require custom validation logic that captures your specific business rules while integrating smoothly with web frameworks and configuration systems.

This section shows you how to implement practical custom validation patterns, integrate Pydantic models with FastAPI for automatic API documentation, and manage application settings through environment variables using the .env file approach that most production applications rely on.

Field validators and model validation
When business logic determines data validity, Pydantic’s @field_validator decorator transforms your validation functions into part of the model itself. Consider a user registration system where different subscription tiers have different password requirements:

from pydantic import BaseModel, field_validator, Field
import re

class UserRegistration(BaseModel):
   username: str = Field(min_length=3)
   email: EmailStr
   password: str
   subscription_tier: str = Field(pattern=r'^(free|pro|enterprise)$')
  
   @field_validator('password')
   @classmethod
   def validate_password_complexity(cls, password, info):
       tier = info.data.get('subscription_tier', 'free')
      
       if len(password) < 8:
           raise ValueError('Password must be at least 8 characters')
          
       if tier == 'enterprise' and not re.search(r'[A-Z]', password):
           raise ValueError('Enterprise accounts require uppercase letters')
          
       return password



#The @field_validator decorator gives you access to other field values through the info.data parameter, allowing validation rules that depend on multiple fields. The validator runs after basic type checking passes, so you can safely assume the subscription_tier is one of the allowed values.

#For validation that spans multiple fields, the @model_validator decorator runs after all individual fields are validated:

from datetime import datetime
from pydantic import model_validator

class EventRegistration(BaseModel):
   start_date: datetime
   end_date: datetime
   max_attendees: int = Field(gt=0)
   current_attendees: int = Field(ge=0)
  
   @model_validator(mode='after')
   def validate_event_constraints(self):
       if self.end_date <= self.start_date:
           raise ValueError('Event end date must be after start date')
          
       if self.current_attendees > self.max_attendees:
           raise ValueError('Current attendees cannot exceed maximum')
          
       return self


#The mode='after' parameter ensures the validator receives a fully constructed model instance, making it perfect for business logic that requires access to all validated fields. The validator must return self to indicate successful validation.

#FastAPI integration
#FastAPI’s integration with Pydantic creates automatic request validation and API documentation. The key pattern involves creating separate models for different operations, giving you control over what data flows in each direction:


from fastapi import FastAPI
from typing import Optional
from datetime import datetime

app = FastAPI()

class UserCreate(BaseModel):
   username: str = Field(min_length=3)
   email: EmailStr
   password: str = Field(min_length=8)

class UserResponse(BaseModel):
   id: int
   username: str
   email: EmailStr
   created_at: datetime
  
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
   # FastAPI automatically validates the request body
   new_user = {
       "id": 1,
       "username": user.username,
       "email": user.email,
       "created_at": datetime.now()
   }
   return UserResponse(**new_user)


#The separation between input and output models provides several benefits. Input models can include validation rules and required fields, while output models control exactly what data gets sent to clients. FastAPI automatically generates OpenAPI documentation from your Pydantic models, creating interactive API docs that developers can use to test endpoints.

#For update operations, you can create models where all fields are optional:
class UserUpdate(BaseModel):
   username: Optional[str] = Field(None, min_length=3)
   email: Optional[EmailStr] = None

@app.patch("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate):
   # Only update provided fields
   update_data = user_update.model_dump(exclude_unset=True)
   # Your database update logic here
   return {"message": f"Updated user {user_id}"}

   #The exclude_unset=True parameter in PATCH operations ensures you only update fields that were explicitly provided, preventing accidental overwrites. This pattern works perfectly for REST APIs where clients send partial updates.

#Configuration management with environment variables
#Production applications need secure, deployment-friendly configuration management. Pydantic’s BaseSettings combined with .env files provides type-safe configuration that works across development, staging, and production environments.

#First, create a .env file in your project root:

# .env file
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
SECRET_KEY=your-secret-key-here
DEBUG=false
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com


#Then define your settings model:
from pydantic import BaseSettings, Field
from typing import List

class AppSettings(BaseSettings):
   database_url: str = Field(description="Database connection URL")
   secret_key: str = Field(description="Secret key for JWT tokens")
   debug: bool = Field(default=False)
   allowed_hosts: List[str] = Field(default=["localhost"])
  
   class Config:
       env_file = ".env"
       case_sensitive = False

# Load settings automatically from environment and .env file
settings = AppSettings()

#The BaseSettings class automatically reads from environment variables, .env files, and command-line arguments. Environment variables take precedence over .env file values, making it easy to override settings in different deployment environments. The case_sensitive = False setting allows flexible environment variable naming.

#For complex applications, you can organize settings into logical groups:

class DatabaseSettings(BaseSettings):
   url: str = Field(env="DATABASE_URL")
   max_connections: int = Field(default=5, env="DB_MAX_CONNECTIONS")

class AppSettings(BaseSettings):
   secret_key: str
   debug: bool = False
   database: DatabaseSettings = DatabaseSettings()
  
   class Config:
       env_file = ".env"

settings = AppSettings()
# Access nested configuration
db_url = settings.database.url


#This nested approach keeps related settings together while maintaining a clear separation between different components of your application. Each settings group can have its own environment variable prefix and validation rules.

#The .env file approach works with deployment platforms like Heroku, AWS, and Docker, where environment variables are the standard way to configure applications. Your application gets type safety and validation while following cloud-native configuration patterns that operations teams expect.

#These patterns form the foundation for building maintainable applications that handle real-world complexity. Pydantic’s validation system adapts to your specific requirements while providing clear error messages and automatic documentation that helps your entire team understand the data structures your application expects.

#Conclusion
#You’ve now seen how Pydantic can save you from the tedious work of writing validation code by hand. Instead of cluttering your functions with isinstance() checks and custom error handling, you can define your data structure once and let Pydantic handle the rest
