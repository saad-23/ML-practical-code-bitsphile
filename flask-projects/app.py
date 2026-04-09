from flask import Flask, render_template,request


# initialize the Flask app
app = Flask(__name__)



# routing 

@app.route("/inventory", methods = ["GET", "POST"])
def checkInventory():
    item_prices = {

        "mobile": 30000,
        "laptop" : 60000,
        "earbuds" : 2000
    }
    if request.method == "POST":
        items = request.form.getlist("items")
        print(items)


    return render_template("inventory.html")

@app.route("/checkadmission",methods = ["GET","POST"])
def checkAdmission():
    global username
    username = ""
    global age
    age = ""
    global marks
    marks = ""
    global status
    status = ""

    if(request.method == "POST"):
        username = request.form.get("username")
        age = request.form.get("age")
        marks = request.form.get("marks")

        print(request.form)
        # request.form.getlist("items") # getting checkboxes values (multiple)

        

        if(int(age) >= 20 and int(marks) >= 70):
            status = f"Yes {username} you are eligible"
        else:
            status = f"No!!! you {username} are not eligible"

    return render_template("admission.html",status = status)



@app.route("/register" , methods = ["GET","POST"] )
def register():
    global username
    username = ""
    if(request.method == "POST"):
        print(request.form.getlist("skill"))
        username = request.form.get("username")


    return render_template("register_form.html",username = username)




@app.route("/form",methods = ['GET','POST'])
def form():
    
    method_type = request.method
    return render_template("form.html",method_type = method_type)

@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    all_recipes = [
        {
            "name": "Scrambled Eggs",
            "cook_time": 10,
            "ingredients": ["3 eggs", "2 tbsp butter", "salt", "pepper", "2 tbsp milk"]
        },
        {
            "name": "Pasta Aglio e Olio",
            "cook_time": 20,
            "ingredients": ["200g spaghetti", "4 garlic cloves", "3 tbsp olive oil", "chili flakes", "parsley", "salt"]
        },
        {
            "name": "Beef Stew",
            "cook_time": 90,
            "ingredients": ["500g beef", "3 potatoes", "2 carrots", "onion", "beef stock", "tomato paste"]
        },
        {
            "name": "Grilled Cheese Sandwich",
            "cook_time": 15,
            "ingredients": ["2 bread slices", "2 cheese slices", "1 tbsp butter"]
        },
        {
            "name": "Chicken Biryani",
            "cook_time": 75,
            "ingredients": ["500g chicken", "2 cups basmati rice", "onion", "yogurt", "biryani spices", "ghee", "saffron"]
        },
        {
            "name": "Veggie Stir Fry",
            "cook_time": 15,
            "ingredients": ["bell pepper", "broccoli", "carrot", "soy sauce", "garlic", "sesame oil", "spring onion"]
        },
        {
            "name": "Avocado Toast",
            "cook_time": 10,
            "ingredients": ["2 bread slices", "1 avocado", "lemon juice", "salt", "chili flakes", "olive oil"]
        },
        {
            "name": "Tomato Soup",
            "cook_time": 25,
            "ingredients": ["4 tomatoes", "1 onion", "2 garlic cloves", "vegetable stock", "cream", "basil", "salt", "pepper"]
        },
        {
            "name": "Dal Tadka",
            "cook_time": 40,
            "ingredients": ["1 cup lentil", "onion", "tomato", "cumin", "mustard seeds", "turmeric", "ghee", "garlic"]
        },
        {
            "name": "Omelette",
            "cook_time": 8,
            "ingredients": ["3 eggs", "onion", "tomato", "green chili", "salt", "butter", "coriander"]
        },
        {
            "name": "Quesadilla",
            "cook_time": 12,
            "ingredients": ["2 flour tortillas", "cheese", "bell pepper", "black beans", "sour cream", "salsa"]
        },
        {
            "name": "Lamb Roast",
            "cook_time": 120,
            "ingredients": ["1kg lamb leg", "rosemary", "garlic", "olive oil", "lemon", "salt", "pepper"]
        },
    ]

    quick_recipes = [r for r in all_recipes if r["cook_time"] < 30]

    search_query = ""
    results = quick_recipes

    if request.method == "POST":
        search_query = request.form.get("search", "").strip().lower()
        if search_query:
            results = [
                r for r in quick_recipes
                if search_query in r["name"].lower()
                or any(search_query in ing.lower() for ing in r["ingredients"])
            ]

    return render_template("recipes.html", results=results, search_query=search_query, total=len(quick_recipes))


@app.route("/")
def test():
    page_title = "My Main Page"
    countries = ["pakistan","england","southafrica"]
    return render_template("test.html",title = page_title , countries = countries)


@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/welcome")
def welcome():
    return render_template("welcome.html")



@app.route("/textreplace")
def textReplace():
    message = "anybody asks me to accept free invite for trial basis of any ai scheme application to use for any purpose"

    updated_message = message

    spam_words = ["free","trial","scheme"]

    for word in spam_words:
        if(word in updated_message): 
            updated_message = updated_message.replace(word,"****")


    return render_template("welcome.html",original_message = message, updated_message = updated_message)
    

# run the flask application

if __name__ == '__main__':
    app.run(debug=True)

