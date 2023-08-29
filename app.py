from flask import Flask, render_template, request
import recommend


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
  if request.method == "POST":
    search_query = request.form.get("q")  # Get the value from the "q" field
    results = recommend.getRecommendations(search_query)
    return render_template("base.html", title="What movie shall we watch?", results=results)

  else:
    return render_template("base.html", title="What movie shall we watch?")

if __name__ == "__main__":
    app.run(debug=True)
