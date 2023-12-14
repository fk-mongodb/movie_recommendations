from pymongo import MongoClient
import gradio as gr
from gradio.themes.base import Base
import recommend


# Create a web interface for trhe app using Gradio
def getRecommendationsAsHTML(topic):
    embedding = recommend.encode(topic)
    cursor = recommend.searchMongoDB(embedding)

    data = list(cursor)  # Convert cursor to a list of dictionaries

    if not data:
        return "No results found."

    # Specify the desired order of columns
    column_order = ["title", "plot", "rating"]

    # Create HTML table
    table_html = "<table>"
    
    # Create table headers in the specified order
    table_html += "<tr>"
    for column in column_order:
        table_html += f"<th>{column.capitalize()}</th>"
    table_html += "</tr>"

    # Populate table rows in the specified order
    for row in data:
        table_html += "<tr>"
        for column in column_order:
            table_html += f"<td>{row.get(column, '')}</td>"
        table_html += "</tr>"

    table_html += "</table>"
    return table_html


with gr.Blocks(theme=Base(), title="MFlix") as demo:
    gr.Markdown(
        """
        # What movie shall we watch?
        The database contains movies with genres of Western, Action, and Fantasy
        """
    )
    textbox = gr.Textbox(label="Describe your movie...")
    with gr.Row():
        button = gr.Button("Submit", variant="primary")

    with gr.Row():
        movies = gr.HTML()

    # Call query_data function upon clicking the Submit button
    button.click(getRecommendationsAsHTML, textbox, movies)


# Launch the Gradio Interface
if __name__ == "__main__":
    demo.launch()
