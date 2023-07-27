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
    return render_template('web.html')

'''@app.route('/carbondubai', methods=['GET'])
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
        return jsonify({'error': 'Unsupported file format.'}), 400'''



@app.route('/carbondubai', methods=['POST'])
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

    #return "File uploaded sucessfully"


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
    '''if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file found.'}), 400

    pdf_file = request.files['pdf2']

    if pdf_file.filename == '':
        return jsonify({'error': 'Invalid PDF file.'}), 400

    extracted_texts = extract_text_from_pdf(pdf_file)
    #return jsonify({"pages" : extracted_texts})
    carbon = extracted_texts[0]['lines'].index("upto 800")
    return jsonify({"carbon emission" : str(extracted_texts[0]['lines'][carbon-1]) + " kg CO2e"})'''

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
    '''if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file found.'}), 400'''

    '''if 'pdf' in request.files:
        pdf_file = request.files['pdf3']
        if pdf_file.filename == '':
            return jsonify({'error': 'Invalid PDF file.'}), 400
        extracted_texts = extract_text_from_pdf(pdf_file)
        #return jsonify({"pages" : extracted_texts})
        kwh = extracted_texts[0]['lines'].index("Consumption")
        carbon = float(extracted_texts[0]['lines'][kwh+1]) * 0.40
        return jsonify({"carbon emission" : str(carbon) + " kg CO2e"})


    elif 'jpg' in request.files:
        jpg_file = request.files['pdf3']
        if jpg_file.filename == '':
            return jsonify({'error': 'Invalid JPG file.'}), 400
        extracted_texts = extract_text_from_image(Image.open(jpg_file))
        # Add any further processing if needed
        return jsonify({"pages": extracted_texts})

    else:
        return jsonify({'error': 'No PDF or JPG file found.'}), 400'''

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
    return jsonify({"total carbon emission": str(carbon_emission) + " t CO2e"})


@app.route('/electricity', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files.get('file')
    emirate = request.form.get('emirate')

    if file.filename == '':
        return "No selected file"

    # Handle the file based on the selected emirate
    if emirate == 'Dubai':
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
                pass

    elif emirate == 'Abu Dhabi':
        if file.filename.lower().endswith('.pdf'):
            extracted_texts = extract_text_from_pdf(file)
            # Add any further processing if needed
            kwh = extracted_texts[2]['lines'].index("Total units")
            carbon = float(extracted_texts[2]['lines'][kwh+1]) * 0.39
            return jsonify({"carbon emission" : str(carbon) + " kg CO2e"})

        elif file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            extracted_texts = extract_text_from_image(Image.open(file))
            # Add any further processing if needed
            kwh1 = extracted_texts.index("Total units")
            carbon1 = float(extracted_texts[kwh1+1]) * 0.39
            return jsonify({"carbon emission" : str(carbon1) + " kg CO2e"})
            #return jsonify({"pages" : extracted_texts})


        else:
            return jsonify({'error': 'Unsupported file format.'}), 400
            pass

    elif emirate == 'Sharjah':
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

    elif emirate == 'Umm Al Quwain':
        if file.filename.lower().endswith('.pdf'):
            extracted_texts = extract_text_from_pdf(file)
            # Add any further processing if needed
            carbon = extracted_texts[0]['lines'].index("upto 800")
            return jsonify({"carbon emission" : str(carbon-1) + " kg CO2e"})

        elif file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            extracted_texts = extract_text_from_image(Image.open(file))
            carbon = extracted_texts.index("upto 800")
            return jsonify({"carbon emission" : str(extracted_texts[carbon-1]) + " kg CO2e"})
        else:
            return jsonify({'error': 'Unsupported file format.'}), 400
    else:
        return "Invalid emirate selection"

    return "File uploaded and processed successfully"








