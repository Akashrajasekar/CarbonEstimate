import os
import io
from pdf2image import convert_from_bytes
from flask import Flask, request, jsonify, render_template
from google.cloud import vision_v1
from PIL import Image
import requests
import json
import mysql.connector

app = Flask(__name__)
db_config = {
    'host': 'CarbonEstimate.mysql.pythonanywhere-services.com',
    'user': 'CarbonEstimate',
    'password': 'Verofax123',
    'database': 'CarbonEstimate$default'
}
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/CarbonEstimate/credentials.json'


def extract_text_from_image(image):
    client = vision_v1.ImageAnnotatorClient()

    # Convert PIL Image to bytes
    with io.BytesIO() as output:
        image.save(output, format='PNG')
        content = output.getvalue()

    input_image = vision_v1.Image(content=content)

    # Perform text detection on the image
    response = client.text_detection(image=input_image)

    extracted_text = response.text_annotations[0].description

    lines = extracted_text.split('\n')

    return lines

def extract_text_from_pdf(pdf_file):
    images = convert_from_bytes(pdf_file.read(), dpi=300)  # Adjust dpi as needed

    extracted_texts = []

    for i, image in enumerate(images):
        lines = extract_text_from_image(image)
        extracted_texts.append({'page': i + 1 , 'lines': lines})

    return extracted_texts

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/electricity.html')
def electricity():
    return render_template('electricity.html')

@app.route('/vehicle.html')
def vehiclepage():
    return render_template('vehicle.html')

@app.route('/flight.html')
def flightpage():
    return render_template('flight.html')

@app.route('/results.html')
def results():
    return render_template('results.html')



@app.route('/carbondubai', methods=['GET'])
def extract_text_dubai():
    if 'file1' not in request.files:
        return jsonify({'error': 'No file found.'}), 400

    file = request.files['file1']
    if file.filename == '':
        return jsonify({'error': 'Invalid file.'}), 400

    if file.filename.lower().endswith('.pdf'):
        extracted_texts = extract_text_from_pdf(file)
        # Add any further processing if needed
        carbon = extracted_texts[1]['lines'].index("Kg CO2e")
        return jsonify({"carbon emission" : str(extracted_texts[1]['lines'][carbon+1]) + " kg CO2e"})

    elif file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        extracted_texts = extract_text_from_image(Image.open(file))
        # Add any further processing if needed
        carbon = extracted_texts.index("Kg CO2e")
        return jsonify({"carbon emission" : str(extracted_texts[carbon+1]) + " kg CO2e"})


    else:
        return jsonify({'error': 'Unsupported file format.'}), 400


@app.route('/carbonabud', methods=['GET'])
def extract_text_abu():

    if 'file0' not in request.files:
        return jsonify({'error': 'No file found.'}), 400

    inp_file = request.files['file0']
    if inp_file.filename == '':
        return jsonify({'error': 'Invalid file.'}), 400

    if inp_file.filename.lower().endswith('.pdf'):
        extracted_texts = extract_text_from_pdf(inp_file)
        # Add any further processing if needed
        kwh = extracted_texts[2]['lines'].index("Total units")
        carbon = float(extracted_texts[2]['lines'][kwh+1]) * 0.39
        return jsonify({"carbon emission" : str(carbon) + " kg CO2e"})

    elif inp_file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        extracted_texts = extract_text_from_image(Image.open(inp_file))
        # Add any further processing if needed
        kwh1 = extracted_texts.index("Total units")
        carbon1 = float(extracted_texts[kwh1+1]) * 0.39
        return jsonify({"carbon emission" : str(carbon1) + " kg CO2e"})
        #return jsonify({"pages" : extracted_texts})


    else:
        return jsonify({'error': 'Unsupported file format.'}), 400



@app.route('/carbonfewa', methods=['GET'])
def extract_text_fewa():
    if 'file01' not in request.files:
        return jsonify({'error': 'No file found.'}), 400

    inp_file = request.files['file01']
    if inp_file.filename == '':
        return jsonify({'error': 'Invalid file.'}), 400

    if inp_file.filename.lower().endswith('.pdf'):
        extracted_texts = extract_text_from_pdf(inp_file)
        # Add any further processing if needed
        carbon = extracted_texts[0]['lines'].index("upto 800")
        return jsonify({"carbon emission" : str(carbon-1) + " kg CO2e"})

    elif inp_file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        extracted_texts = extract_text_from_image(Image.open(inp_file))
        carbon = extracted_texts.index("upto 800")
        return jsonify({"carbon emission" : str(extracted_texts[carbon-1]) + " kg CO2e"})


    else:
        return jsonify({'error': 'Unsupported file format.'}), 400




@app.route('/carbonshrj', methods=['GET'])
def extract_text_shrj():
    if 'file' not in request.files:
        return jsonify({'error': 'No file found.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Invalid file.'}), 400

    if file.filename.lower().endswith('.pdf'):
        extracted_texts = extract_text_from_pdf(file)
        # Add any further processing if needed
        kwh = extracted_texts[0]['lines'].index("Consumption")
        carbon = float(extracted_texts[0]['lines'][kwh+1]) * 0.40
        return jsonify({"carbon emission" : str(carbon) + " kg CO2e"})

    elif file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        extracted_texts = extract_text_from_image(Image.open(file))
        # Add any further processing if needed
        #return jsonify({"pages": extracted_texts})
        kwh = extracted_texts.index("Previous Reading Date Consumption")
        carbon = float(extracted_texts[kwh+2]) * 0.40
        return jsonify({"carbon emission" : str(carbon) + " kg CO2e"})


    else:
        return jsonify({'error': 'Unsupported file format.'}), 400


@app.route('/carbonflight', methods=['POST'])
def flight():
    url = "https://www.carboninterface.com/api/v1/estimates"
    headers = {
        "Authorization": "Bearer Eq8vmxlGJFDQJWlxXPb5A",
        "Content-Type": "application/json"
    }
    passengers = request.form["passengers"]
    num_legs = int(request.form.get("Trips", 1))  # Number of trips, defaulting to 1 if not provided

    legs = []
    for i in range(1, num_legs + 1):
        departure_airport = request.form[f"From{i}"]
        destination_airport = request.form[f"To{i}"]
        legs.append({
            "departure_airport": departure_airport,
            "destination_airport": destination_airport
        })

    payload = {
        "type": "flight",
        "passengers": passengers,
        "legs": legs,
        "distance_unit": "km",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    carbon_trans = response.json()["data"]["attributes"]["carbon_kg"]
    return jsonify({"carbon emission due to flight": str(carbon_trans) + " kg C02e"})

def flight1():
    url = "https://www.carboninterface.com/api/v1/estimates"
    headers = {
        "Authorization": "Bearer Eq8vmxlGJFDQJWlxXPb5A",
        "Content-Type": "application/json"
    }
    passengers = request.form["passengers"]
    num_legs = int(request.form.get("Trips", 1))  # Number of trips, defaulting to 1 if not provided

    legs = []
    for i in range(1, num_legs + 1):
        departure_airport = request.form[f"From{i}"]
        destination_airport = request.form[f"To{i}"]
        legs.append({
            "departure_airport": departure_airport,
            "destination_airport": destination_airport
        })

    payload = {
        "type": "flight",
        "passengers": passengers,
        "legs": legs,
        "distance_unit": "km",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    carbon_trans = response.json()["data"]["attributes"]["carbon_kg"]
    return float(carbon_trans)


@app.route('/carbonvehicle', methods=['POST'])
def vehicle():
        num_veh = int(request.form.get("vehicle_no",1))

        veh = []
        for i in range(1, num_veh + 1):
            veh_type = request.form[f"Vehicle{i}"]
            fuel = request.form[f"Fuel Type{i}"]
            distance = float(request.form[f"Distance{i}"])

            emission = trans_emission(fuel, veh_type, distance)
            veh.append(emission)

        tot = sum(veh)

        return jsonify({"carbon emission due to vehicles": str(tot) + " kg CO2e"})

def vehicle1():
    num_veh = int(request.form.get("vehicle_no",1))

    veh = []
    for i in range(1, num_veh + 1):
        veh_type = request.form[f"Vehicle{i}"]
        fuel = request.form[f"Fuel Type{i}"]
        distance = float(request.form[f"Distance{i}"])

        emission = trans_emission(fuel, veh_type, distance)
        veh.append(emission)

    tot = sum(veh)

    return tot

def trans_emission(fuel, veh_type, distance):
    try:
        conn = mysql.connector.connect(**db_config)
        # Execute SQL query
        cursor = conn.cursor()
        if veh_type == "Compact car":
            query = 'SELECT compact_car, emission_factor FROM fueldata WHERE name=%s'
            val = (fuel,)
            cursor.execute(query, val)
        elif veh_type == "Mid-range car":
            query = 'SELECT midrange_car, emission_factor FROM fueldata WHERE name=%s'
            val = (fuel,)
            cursor.execute(query, val)
        elif veh_type == "Luxury / SUV / Van":
            query = 'SELECT luxury_car, emission_factor FROM fueldata WHERE name=%s'
            val = (fuel,)
            cursor.execute(query, val)


        result = cursor.fetchone()
        emission_factor = result[0]
        fuel_con = result[1]

        # Close MySQL connection
        conn.close()

    except Exception as e:

        return str(e)

    total_fuel_consumed = float(fuel_con) * distance
    emission = float(emission_factor) * total_fuel_consumed

    return emission

@app.route('/offset', methods=['GET'])
def offset():
    carbonoffset=220.2*(float(request.args.get('total_emission')))
    return jsonify({"offset" : str(carbonoffset)})

@app.route('/carbontotal', methods=['GET'])
def carbon_total():
    total=[]
    emirate = request.form.get('emirate')

    if not emirate:
        return {'error': 'Emirate value not provided.'}

    emirate = emirate.lower()

    if emirate not in ['dubai', 'abudhabi', 'sharjah', 'fewa']:
        return {'error': 'Invalid emirate. Supported emirates are: dubai, abudhabi, sharjah, fewa'}

    file_key = 'file_t'

    if file_key not in request.files:
        return {'error': 'No file found.'}

    inp_file = request.files[file_key]
    if inp_file.filename == '':
        return {'error': 'Invalid file.'}

    if inp_file.filename.lower().endswith('.pdf'):
            extracted_texts = extract_text_from_pdf(inp_file)
            # Add any further processing if needed

            if emirate == 'abudhabi':
                kwh = extracted_texts[2]['lines'].index("Total units")
                carbon = float(extracted_texts[2]['lines'][kwh+1]) * 0.39
            elif emirate == 'dubai':
                carbon = extracted_texts[1]['lines'].index("Kg CO2e")
                carbon = float(extracted_texts[1]['lines'][carbon+1])
            elif emirate == 'sharjah':
                kwh = extracted_texts[0]['lines'].index("Consumption")
                carbon = float(extracted_texts[0]['lines'][kwh+1]) * 0.40
            elif emirate == 'fewa':
                carbon = extracted_texts[0]['lines'].index("upto 800")
                carbon = float(extracted_texts[0]['lines'][carbon-1])

            total.append(carbon)

    elif inp_file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            extracted_texts = extract_text_from_image(Image.open(inp_file))
            # Add any further processing if needed

            if emirate == 'abudhabi':
                kwh1 = extracted_texts.index("Total units")
                carbon1 = float(extracted_texts[kwh1+1]) * 0.39
            elif emirate == 'dubai':
                carbon = extracted_texts.index("Kg CO2e")
                carbon1 = float(extracted_texts[carbon+1])
            elif emirate == 'sharjah':
                kwh = extracted_texts.index("Previous Reading Date Consumption")
                carbon1 = float(extracted_texts[kwh+2]) * 0.40
            elif emirate == 'fewa':
                carbon = extracted_texts.index("upto 800")
                carbon1 = float(extracted_texts[carbon-1])

            total.append(carbon1)

    else:
        return {'error': 'Unsupported file format.'}

    veh_tot=vehicle1();
    total.append(veh_tot)
    fly_tot=flight1()
    total.append(fly_tot)

    carbon_emission=sum(total)/1000
    price=calculate_money_for_carbon_offset(carbon_emission)
    return jsonify({"total carbon emission": str(carbon_emission) + " t CO2e",
                    "Offset price": "AED. " +str(price) })


'''@app.route('/electricity', methods=['POST'])
def upload():
    total=[]
    emirate = request.form.get('emirate')

    if not emirate:
        return {'error': 'Emirate value not provided.'}

    emirate = emirate.lower()

    if emirate not in ['dubai', 'abu dhabi', 'sharjah', 'ajman', 'fujairah', 'umm al quwain', 'ras al khaimah']:
        return {'error': 'Invalid emirate. Supported emirates are: dubai, abudhabi, sharjah, fewa'}


    inp_file = request.files.get('file')

    if inp_file is None or inp_file.filename == '':
        return {'error': 'Invalid file.'}

    if inp_file.filename.lower().endswith('.pdf'):
            extracted_texts = extract_text_from_pdf(inp_file)
            # Add any further processing if needed

            if emirate == 'abu dhabi':
                kwh = extracted_texts[2]['lines'].index("Total units")
                carbon = float(extracted_texts[2]['lines'][kwh+1]) * 0.39
            elif emirate == 'dubai':
                carbon = extracted_texts[1]['lines'].index("Kg CO2e")
                carbon = float(extracted_texts[1]['lines'][carbon+1])
            elif emirate == 'sharjah':
                kwh = extracted_texts[0]['lines'].index("Consumption")
                carbon = float(extracted_texts[0]['lines'][kwh+1]) * 0.40
            elif emirate == 'ajman' or emirate == 'fujairah' or emirate == 'umm al quwain' or emirate == 'ras al khaimah' :
                carbon = extracted_texts[0]['lines'].index("upto 800")
                carbon = float(extracted_texts[0]['lines'][carbon-1])

            total.append(carbon)

    elif inp_file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            extracted_texts = extract_text_from_image(Image.open(inp_file))
            # Add any further processing if needed

            if emirate == 'abu dhabi':
                kwh1 = extracted_texts.index("Total units")
                carbon1 = float(extracted_texts[kwh1+1]) * 0.39
            elif emirate == 'dubai':
                carbon = extracted_texts.index("Kg CO2e")
                carbon1 = float(extracted_texts[carbon+1])
            elif emirate == 'sharjah':
                kwh = extracted_texts.index("Previous Reading Date Consumption")
                carbon1 = float(extracted_texts[kwh+2]) * 0.40
            elif emirate == 'ajman' or emirate == 'fujairah' or emirate == 'umm al quwain' or emirate == 'ras al khaimah' :
                carbon = extracted_texts.index("upto 800")
                carbon1 = float(extracted_texts[carbon-1])

            total.append(carbon1)

    else:
        return {'error': 'Unsupported file format.'}

    num_veh = int(request.form.get("vehicle_no", 1))

    if num_veh!=0:
        veh = []
        for i in range(1, num_veh + 1):
            veh_type = request.form.get(f"Vehicle{i}")
            fuel = request.form.get(f"Fuel Type{i}")
            distance = float(request.form.get(f"Distance{i}"))

            emission = trans_emission(fuel, veh_type, distance)
            veh.append(emission)

        veh_tot = sum(veh)
    else:
        veh_tot=0

    total.append(veh_tot)

    url = "https://www.carboninterface.com/api/v1/estimates"
    headers = {
        "Authorization": "Bearer Eq8vmxlGJFDQJWlxXPb5A",
        "Content-Type": "application/json"
    }
    passengers = request.form["passengers"]
    num_legs = int(request.form.get("Trips", 1))  # Number of trips, defaulting to 1 if not provided

    if (num_legs != 0 and passengers != 0) or num_legs != 0:
        legs = []
        for i in range(1, num_legs + 1):
            departure_airport = request.form[f"From{i}"]
            destination_airport = request.form[f"To{i}"]
            legs.append({
                "departure_airport": departure_airport,
                "destination_airport": destination_airport
            })

        payload = {
            "type": "flight",
            "passengers": passengers,
            "legs": legs,
            "distance_unit": "km",
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        carbon_trans = response.json()["data"]["attributes"]["carbon_kg"]
    else:
        carbon_trans = 0

    total.append(float(carbon_trans))



    carbon_emission=sum(total)/1000
    return jsonify({"total_carbon_emission": str(carbon_emission) + " t CO2e"})'''


@app.route('/electricity', methods=['POST'])
def upload():
    emirate = request.form.get('emirate')

    if not emirate:
        return {'error': 'Emirate value not provided.'}

    emirate = emirate.lower()

    if emirate not in ['dubai', 'abu dhabi', 'sharjah', 'ajman', 'fujairah', 'umm al quwain', 'ras al khaimah']:
        return {'error': 'Invalid emirate. Supported emirates are: dubai, abudhabi, sharjah, fewa'}

    inp_file = request.files.get('file')

    if inp_file is None or inp_file.filename == '':
        return {'error': 'Invalid file.'}

    if inp_file.filename.lower().endswith('.pdf'):
        extracted_texts = extract_text_from_pdf(inp_file)
        # Add any further processing if needed

        if emirate == 'abu dhabi':
            kwh = extracted_texts[2]['lines'].index("Total units")
            carbon1 = (float(extracted_texts[2]['lines'][kwh + 1]) * 0.39)/1000
        elif emirate == 'dubai':
            carbon = extracted_texts[1]['lines'].index("Kg CO2e")
            carbon1 = (float(extracted_texts[1]['lines'][carbon + 1]))/1000
        elif emirate == 'sharjah':
            kwh = extracted_texts[0]['lines'].index("Consumption")
            carbon1 = (float(extracted_texts[0]['lines'][kwh + 1]) * 0.40)/1000
        elif emirate in ['ajman', 'fujairah', 'umm al quwain', 'ras al khaimah']:
            carbon = extracted_texts[0]['lines'].index("upto 800")
            carbon1 = (float(extracted_texts[0]['lines'][carbon - 1]))/1000
        else:
            return {'error': 'Unsupported emirate.'}

    elif inp_file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        extracted_texts = extract_text_from_image(Image.open(inp_file))
        # Add any further processing if needed

        if emirate == 'abu dhabi':
            kwh1 = extracted_texts.index("Total units")
            carbon1 = (float(extracted_texts[kwh1 + 1]) * 0.39)/1000
        elif emirate == 'dubai':
            carbon = extracted_texts.index("Kg CO2e")
            carbon1 = (float(extracted_texts[carbon + 1]))/1000
        elif emirate == 'sharjah':
            kwh = extracted_texts.index("Previous Reading Date Consumption")
            carbon1 = (float(extracted_texts[kwh + 2]) * 0.40)/1000
        elif emirate in ['ajman', 'fujairah', 'umm al quwain', 'ras al khaimah']:
            carbon = extracted_texts.index("upto 800")
            carbon1 = (float(extracted_texts[carbon - 1]))/1000
        else:
            return {'error': 'Unsupported emirate.'}

    else:
        return {'error': 'Unsupported file format.'}


    return jsonify({"total_carbon_emission": str(carbon1)})




@app.route('/vehicle2', methods=['POST'])
def vehicle2():
    num_veh = int(request.form.get("vehicle_no", 1))

    if num_veh!=0:
        veh = []
        for i in range(1, num_veh + 1):
            veh_type = request.form.get(f"Vehicle{i}")
            fuel = request.form.get(f"Fuel Type{i}")
            distance = float(request.form.get(f"Distance{i}"))

            emission = trans_emission(fuel, veh_type, distance)
            veh.append(emission)

        veh_tot = sum(veh)/1000
    else:
        veh_tot=0
    return jsonify({"vehicle_emission": str(veh_tot)})

@app.route('/flight2', methods=['POST'])
def flight2():
    url = "https://www.carboninterface.com/api/v1/estimates"
    headers = {
            "Authorization": "Bearer Eq8vmxlGJFDQJWlxXPb5A",
            "Content-Type": "application/json"
        }
    passengers = request.form["passengers"]
    num_legs = int(request.form.get("Trips", 1))  # Number of trips, defaulting to 1 if not provided

    if (num_legs != 0 and passengers != 0) or num_legs != 0:
            legs = []
            for i in range(1, num_legs + 1):
                departure_airport = request.form[f"From{i}"]
                destination_airport = request.form[f"To{i}"]
                legs.append({
                    "departure_airport": departure_airport,
                    "destination_airport": destination_airport
                })

            payload = {
                "type": "flight",
                "passengers": passengers,
                "legs": legs,
                "distance_unit": "km",
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))
            carbon_trans =float(response.json()["data"]["attributes"]["carbon_mt"])
    else:
            carbon_trans = 0
    return jsonify({"flight_emission": str(carbon_trans) })



