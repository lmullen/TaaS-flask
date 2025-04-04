from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

import csv

# A dictionary of years pointing to events
events = {}

with open("events.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        events[int(row["year"])] = row["event"]


@app.route("/hello")
def hello_world():
    return "This is a timeline web app."


@app.route("/about")
def about():
    return "This timeline was made using Flask."


@app.route("/")
def root_redirect():
    return redirect(url_for("events_html"))


@app.route("/year/<int:year>.txt")
def year_text(year):
    # Version 1
    return events.get(year)

    # Version 2
    # event = events.get(year)
    # if event is not None:
    #     return f"{year}: {event}", 200, {"Content-Type": "text/plain; charset=utf-8"}
    # else:
    #     return (
    #         f"{year}: No event happened in that year.",
    #         200,
    #         {"Content-Type": "text/plain; charset=utf-8"},
    #     )


@app.route("/event")
def year_query():
    year = request.args.get("year", type=int)
    return events.get(year)


@app.route("/year/<int:year>")
def year_html(year):
    event = events.get(year)

    # Version 1
    if event is not None:
        return f"<h1>Timeline as a Service</h1><p><strong>{year}</strong>: {event}</p>"
    else:
        return f"<h1>Timeline as a Service</h1><p><strong>{year}</strong>: No event happened in that year.</p>"

    # Version 2
    # return render_template("year.html", year=year, event=event)


@app.route("/year/<int:year>.json")
def year_json(year):
    event = events.get(year)

    return {
        "year": year,
        "event": event,
    }


@app.route("/events")
def events_html():
    events_sorted = dict(sorted(events.items()))
    return render_template("events.html", events=events_sorted)


@app.route("/events.json")
def events_json():
    # version 1
    return events

    # version 2
    # return [{"year": year, "event": events.get(year)} for year in events]


@app.route("/year/")
def years_redirect():
    return redirect(url_for("events_html"))


@app.route("/events/new", methods=["GET", "POST"])
def new_event():
    if request.method == "POST":
        input = request.get_json()
        events.setdefault(input.get("year"), input.get("event"))
        return redirect(url_for("events_html"))
    else:
        return render_template("new.html")
