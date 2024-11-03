from flask import render_template, url_for, request, redirect, session
from flask import current_app as app
from .forms import LocationForm, DataForm
from . import db
from nominatim_requests import queryLocation
from weather_data import cmip6, readNC
from utils import extract_zipfile
import ast
import glob
from .models import Config, Precipitation


@app.route("/")
def index():
    # Write some logic to reroute to dashboard or setup
    if Precipitation.query.count() == 0:
        return redirect(url_for("setup"))
    else:
        return render_template("index.jinja2")


@app.route("/setup", methods=["GET"])
def setup():
    # User should not access this page if data is already downloaded
    if Precipitation.query.count() != 0:
        return redirect("/dashboard")
    else:
        form = LocationForm()
        return render_template("setup.jinja2", form=form)


@app.route("/setup/location", methods=["POST"])
def location():
    location = request.form.get("location")
    res = queryLocation(location)
    return render_template("setup.jinja2", res=res)


@app.route("/weather_data", methods=["POST"])
def weather_data():
    res = ast.literal_eval(request.form.get("location_selection"))
    lat = round(float(res.get("lat")), 2)
    lon = round(float(res.get("lon")), 2)
    years = list(map(str, list(range(2024, 2029))))

    # .cache naming convention
    filename = f"{lat}-{lon}_{int(len(years))}"
    path = f"./.cache/{filename}"

    # # !!! The instance reloads in debug mode when file is downloaded
    # zipfile = cmip6(lat, lon, years)
    # extract_zipfile(zipfile, path)
    series = readNC(glob.glob(f"{path}/*.nc")[0])

    series.to_sql(
        name="precipitation",
        con=db.engine,
        if_exists="replace",
        index=True,
    )

    init_setup = Config(
        username="admin",
        setup_complete=True,
        location_name=res.get("display_name"),
        location_lat=lat,
        location_lon=lon,
    )
    db.session.add(init_setup)
    db.session.commit()

    return redirect(url_for("settings"))


@app.route("/settings", methods=["GET", "POST"])
def settings():
    form = DataForm()
    if request.method == "POST":
        storage_size = request.form.get("storage_size")
        roof_size = request.form.get("roof_size")
        people = request.form.get("peolple")

        print(storage_size)
        print(roof_size)
        print(people)

        config = Config.query.filter(username = "admin")

        config.storage_size = storage_size
        config.roof_size = roof_size
        config.people = people

        db.session.commit()

        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("settings.jinja2", form=form)
